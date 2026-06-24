from datetime import datetime
from fastapi import FastAPI ,HTTPException
from app.schemas import Expense
from app.databse import init_db ,get_conn

app = FastAPI()
init_db()


@app.get("/")
def home():
    return {"message":"Welcome to expense tracker"}

@app.get("/expenses")

def get_expenses():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")
    data = cur.fetchall()
    conn.close()

    return data

@app.post("/AddExpense")

def add_expense(expense:Expense):
    conn = get_conn()
    cur = conn.cursor()
    curr_time = datetime.now().isoformat()
    cur.execute("""
        INSERT INTO expenses(amount,category,description,created_at)
        VALUES(?,?,?,?)

    """,(expense.amount,expense.category,expense.desc,curr_time))
    conn.commit()
    conn.close()


