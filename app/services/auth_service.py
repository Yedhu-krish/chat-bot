from app.services.user_service import get_user_by_email,get_user_by_username,create_user,get_user_by_identifier
from app.security.password import hash_password,verify_password
from fastapi import HTTPException
from app.services.jwt_service import create_access_token,create_refresh_token
from app.database.models import RefreshToken
from datetime import datetime
from sqlalchemy import select

def register_user(db,username:str,password:str,email:str = None):
    # if (get_user_by_username(db=db,username=username) or get_user_by_email(db=db,email=email)) is not None:
    #     raise HTTPException(status_code=400,detail="User already Exists.")
    exisitng_username = get_user_by_username(db=db,username=username)
    if exisitng_username:
        raise HTTPException(status_code=400,detail=f"Username {username} already Exists.")
    exising_email = get_user_by_email(db=db,email=email)
    if exising_email:
        raise HTTPException(status_code=400,detail=f"A user with {email} already Exists.")
    hashed_password = hash_password(password)
    user = create_user(db,username=username,hashed_password=hashed_password,email=email)
    return user


def login_user(db,identifier:str,password:str):
    user = get_user_by_identifier(db,identifier=identifier)
    if not user:
        raise HTTPException(status_code=401,detail="Invalid username/email or password.")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid username/email or password.")
    
    data = {
        "sub": str(user.id)
    }
    access_token_dict = create_access_token(data=data)
    access_token = access_token_dict["token"]
    refresh_token_dict = create_refresh_token(data=data)
    refresh_token = refresh_token_dict["token"]
    store_refresh_token(db=db,refresh_token=refresh_token,user_id=user.id,expires_at=refresh_token_dict["expires_at"])
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"

    }

def store_refresh_token(db,refresh_token:str,user_id:int,expires_at:datetime):
    token = RefreshToken(token=refresh_token,user_id=user_id,expires_at=expires_at)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def get_refresh_token(db,refresh_token:str):
    stmnt = select(RefreshToken).where(RefreshToken.token == refresh_token)
    result = db.execute(stmnt)
    token = result.scalar_one_or_none()
    return token

def revoke_refresh_token(db,refresh_token:str):
    stmnt = select(RefreshToken).where(RefreshToken.token == refresh_token)
    result = db.execute(stmnt)
    token = result.scalar_one_or_none()
    if token is None:
        raise HTTPException(status_code=404,detail="Token not found!")
    token.revoked= True
    db.commit()
    db.refresh(token)
    return token
    

