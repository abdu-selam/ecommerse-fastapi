from pwdlib import PasswordHash
from uuid import uuid4

password_hash = PasswordHash.recommended()

def hash(password: str):
    return password_hash.hash(password)

def verify(password: str, hashed: str):
    return password_hash.verify(password, hashed)

def gen_token() -> str:
    return str(uuid4())
