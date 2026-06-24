from pydantic import BaseModel

class Expense(BaseModel):
    amount :float
    category:str
    desc :str
    