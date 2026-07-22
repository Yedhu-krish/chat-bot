from app.database.models import User
from sqlalchemy import select

def get_or_create_user(db,username:str):
    stmnt = select(User).where(User.username == username)
    result = db.execute(stmnt)
    user = result.scalar_one_or_none()
    if user is None:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return user


def get_user_by_email(db,email: str):
    stmnt = select(User).where(User.email == email)
    result = db.execute(stmnt)
    user = result.scalar_one_or_none()
    return user

def get_user_by_username(db,username : str):
    stmnt = select(User).where(User.username == username)
    result = db.execute(stmnt)
    user = result.scalar_one_or_none()
    return user

def create_user(db,username:str,hashed_password:str,email:str=None):
    user = User(username=username,email=email,hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db,user_id:int):
    stmnt = select(User).where(User.id==user_id)
    result = db.execute(stmnt)
    user = result.scalar_one_or_none()
    return user

def get_user_by_identifier(db,identifier:str):
    if "@" in identifier:
        return get_user_by_email(db,identifier)
    return get_user_by_username(db,identifier)