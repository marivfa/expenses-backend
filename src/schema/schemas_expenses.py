from typing import List, Optional
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel

from . import schemas_remainders

class ExpensesBase(BaseModel):
    class Config:
        orm_mode = True

class Expenses(ExpensesBase):
    amount : float
    id_user : int
    id_category : int

    real_date : date | None
    comment: str | None
    remainders : schemas_remainders.Remainders | None = None


class ExpensesList(ExpensesBase):
    id: int
    date_register : datetime
    amount : float
    id_user : int
    id_category : int
    
    real_date : date | None
    comment: str | None
    category: str
    user: str
    type : str

class ExpensesUpdate(ExpensesBase):
    amount : float
    category: str
    id_user : int
    id_category : int

    real_date : date | None
    comment: str | None