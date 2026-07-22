import jwt
from app.config import JWT_SECRET_KEY,JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_MINUTES
from datetime import datetime,timezone,timedelta
from fastapi.exceptions import HTTPException

# now = datetime.now(timezone.utc)

# def create_access_token(data:dict) -> str:
#     exp = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     iat = now
#     data_copy = data.copy()
#     data_copy["exp"] = exp
#     data_copy["iat"] = iat
#     token = jwt.encode(payload=data_copy,key=JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)
#     return token


def create_token(data:dict,expires_delta:timedelta,token_type:str) ->dict:
    now = datetime.now(timezone.utc)
    expires_at = now + expires_delta
    data_copy = data.copy()
    data_copy["iat"] = now
    data_copy["exp"] = expires_at
    data_copy["typ"] = token_type
    token = jwt.encode(payload=data_copy,key=JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)
    return {
        "token":token,
        "expires_at":expires_at
    }

def create_access_token(data:dict) -> dict:
    return create_token(data=data,expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),token_type="access")

def create_refresh_token(data:dict) -> dict:
    return create_token(data=data,expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),token_type="refresh")

def decode_token(token:str) -> dict:
    try:
        result = jwt.decode(token,key=JWT_SECRET_KEY,algorithms=[JWT_ALGORITHM])
    except ValueError:
        raise HTTPException(status_code=404,detail="Token Expired/Not found")
    return result