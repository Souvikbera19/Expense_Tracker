from h11._abnf import status_code
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from fastapi import FastAPI ,HTTPException,Depends,status
from app.schemas import Expense,User,UserInDB,TokenData,Token,UserRegister
from app.databse import init_db ,get_conn
from  fastapi.security import OAuth2PasswordBearer
from app.auth import authenticate_user, get_current_active_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,get_curent_user,get_password_hash
from datetime import datetime,timezone,timedelta
import sqlite3
from typing import Annotated
app = FastAPI()
init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def home():
    return {"message":"Welcome to expense tracker"}

@app.post("/register")
def register(user:UserRegister):
    conn = get_conn()
    cur = conn.cursor()
    hashed = get_password_hash(user.password)
    try:
        cur.execute(
            "INSERT INTO users(username,email,full_name,hashed_password) VALUES(?,?,?,?)",
            (user.username,user.email,user.full_name,hashed)
        )
        conn.commit()
        user_id = cur.lastrowid
        conn.close()
        return {"id":user_id,"username":user.username,"email":user.email,"full_name":user.full_name}
    
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )



@app.post("/token")
def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()])->Token:
    user = authenticate_user(form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect Username or Password",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.username},expires_delta=expires_delta
    )
    return Token(access_token=access_token,token_type="bearer")


@app.get("/users/me")
def read_user_me(current_user:Annotated[User,Depends(get_curent_user)]):
    return current_user
    

@app.get("/expenses")
def get_expenses(current_user:User=Depends(get_curent_user)):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT amount,category,description,created_at FROM expenses WHERE user_id=?",
        (current_user.id, )
    )
    data = cur.fetchall()
    conn.close()

    return data


@app.post("/AddExpense")
def add_expense(expense:Expense,current_user:User=Depends(get_curent_user)):
    conn = get_conn()
    cur = conn.cursor()
    curr_time = datetime.now().isoformat()
    cur.execute("""
        INSERT INTO expenses(amount,category,description,created_at,user_id)
        VALUES(?,?,?,?,?)

    """,(expense.amount,expense.category,expense.desc,curr_time,current_user.id))
    conn.commit()
    conn.close()
    return {"message": "Expense added successfully"}

@app.get("/TotalExpenses")
def total_expenses(current_user:User=Depends(get_curent_user)):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?",(current_user.id,))
    total = cur.fetchone()[0]
    conn.close()
    return total or 0
   


