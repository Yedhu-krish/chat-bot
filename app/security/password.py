from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def hash_password(password:str) -> str:
    hashed = password_hasher.hash(password)
    return hashed

def verify_password(password:str,hashed_password:str) -> bool:
    return password_hasher.verify(password,hashed_password)