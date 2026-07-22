from pydantic import BaseModel,EmailStr,field_validator
import re

class RegisterRequest(BaseModel):
    username : str
    email : EmailStr
    password : str

    @field_validator("username")
    @classmethod
    def validate_username(cls,value:str):
        if not re.fullmatch(r"[a-zA-Z0-9_]+", value):
            raise ValueError(
                "Username may contain only letters, numbers, underscores."
            )
        return value

# class LoginRequest(BaseModel):
#     identifier : str
#     password : str

class RefreshTokenRequest(BaseModel):
    refresh_token : str