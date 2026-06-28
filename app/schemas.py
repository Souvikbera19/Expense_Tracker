from os import access
from ipaddress import _BaseAddress
from pydantic import BaseModel

class Expense(BaseModel):
    amount :float
    category:str
    desc :str

class User(BaseModel):
    id: int 
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password:str

class Token(BaseModel):
    access_token :str
    token_type:str

class TokenData(BaseModel):
    username:str

class UserRegister(BaseModel):
    username:str
    password :str
    email:str
    full_name :str
