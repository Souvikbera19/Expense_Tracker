from jwt import InvalidTokenError
from h11._abnf import status_code
from fastapi import status,HTTPException,Depends
from typing import Annotated
import sqlite3
from datetime import datetime,timedelta,timezone
import jwt
from pwdlib import PasswordHash
from app.databse import DATABASE_NAME,get_conn
from app.schemas import UserInDB,TokenData,Token,User
from fastapi.security import OAuth2PasswordBearer
SECRET_KEY = "f25fd43fc6beef38c6e1901d45492d9af4542d285a8bd961be6f762193ce4e4a"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHIM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_hash = PasswordHash.recommended()

def get_password_hash(password:str)->str:
    return password_hash.hash(password)


def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hash.verify(plain_password,hashed_password)

def get_user(username:str):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id,username,email,full_name,hashed_password FROM users WHERE username = ?",(username,))
    data = cur.fetchone()
    conn.close()
    if data:
        return UserInDB(
            id=data["id"],
            username=data["username"],
            email=data["email"],
            full_name=data["full_name"],
            hashed_password=data["hashed_password"]
        )
    return None

def authenticate_user(username:str,password:str):
    user = get_user(username)

    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user


def create_access_token(data:dict,expires_delta:timedelta|None=None)->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHIM)
    return encoded_jwt

def get_curent_user(token:Annotated[str,Depends(oauth2_scheme)]):
    credentail_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHIM)
        username = payload.get("sub")
        if username is None:
            raise credentail_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentail_exception

    user = get_user(username)
    if user is None:
        raise credentail_exception
    
    return user

def get_current_active_user(current_user:Annotated[User,Depends(get_curent_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive User")
    return current_user


    

    
         
        
    