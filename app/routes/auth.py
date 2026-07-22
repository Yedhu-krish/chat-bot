from fastapi.routing import APIRouter
from app.schemas.auth import RegisterRequest,RefreshTokenRequest
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.database import get_db
from app.services.auth_service import register_user,login_user
from app.services.jwt_service import decode_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from app.services.auth_service import get_refresh_token
from app.services.jwt_service import create_access_token,create_refresh_token
import jwt
from datetime import datetime,timezone
from app.services.auth_service import revoke_refresh_token,store_refresh_token


auth_router = APIRouter()

@auth_router.post("/register")
def user_register(request:RegisterRequest,db:Session=Depends(get_db)):
    user = register_user(db=db,username=request.username,password=request.password,email=request.email)
    return {
    "id": user.id,
    "username": user.username
}


# @auth_router.post("/login")
# def user_login(request:LoginRequest,db:Session= Depends(get_db)):
#     return login_user(db=db,password=request.password,identifier=request.identifier)

@auth_router.post("/login")
def user_login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session= Depends(get_db)):
    return login_user(db=db,password=form_data.password,identifier=form_data.username)


@auth_router.post("/refresh")
def refresh(request:RefreshTokenRequest,db:Session=Depends(get_db)):
    refresh_token = request.refresh_token
    try:
        payload = decode_token(refresh_token)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid refresh token")
    if payload["typ"] != "refresh":
        raise HTTPException(status_code=401,detail="Invalid Token Type")
    db_token = get_refresh_token(db=db,refresh_token=refresh_token)
    if not db_token:
        raise HTTPException(status_code=404,detail="Refresh token not found.")
    if db_token.revoked:
        raise HTTPException(status_code=401,detail="Refresh Token has been revoked")
    if db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401,detail="Refresh token expired.")
    revoke_refresh_token(db=db,refresh_token=refresh_token)
    data = {
        "sub":payload["sub"]
    }
    new_refresh_token_dict = create_refresh_token(data=data)
    new_refresh_token = new_refresh_token_dict["token"]
    store_refresh_token(db=db,refresh_token=new_refresh_token,user_id=int(payload["sub"]),expires_at=new_refresh_token_dict["expires_at"])
    new_access_token_dict = create_access_token(data=data)
    new_access_token = new_access_token_dict["token"]
    
    return {
        "access_token":new_access_token,
        "refresh_token":new_refresh_token,
        "token_type":"bearer"
    }