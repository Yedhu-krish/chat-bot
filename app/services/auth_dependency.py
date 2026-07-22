from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.services.jwt_service import decode_token
from app.services.user_service import get_user_by_id
from fastapi.exceptions import HTTPException
from app.database.database import get_db
from sqlalchemy.orm import Session
import jwt
from app.database.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

def get_current_user(db:Session=Depends(get_db),token:str = Depends(oauth2_scheme))-> User:
    try:
        decoded_token = decode_token(token=token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid token.")
    sub = decoded_token.get("sub")
    if sub is None:
        raise HTTPException(status_code=401,detail="Invalid token.")
    user = get_user_by_id(db,user_id=int(sub))
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid authentication credentials.")
    return user
    

