from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from sqlalchemy.orm import Session
from typing import List

from ..config.session import get_db
from ..crud import crud_expenses, crud_remainders
from ..schema import schemas_expenses

from ..auth.auth import get_current_user

router = APIRouter(
    prefix="",
    tags=["expenses"]
)

@router.get("/test")
async def test(username: str = Depends(get_current_user)):
    return {"username": username}

##Expenses
@router.post("/", status_code=201 ,response_model=schemas_expenses.Expenses)
async def create_expenses(expenses: schemas_expenses.Expenses, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    db_expenses = crud_expenses.create_expenses(db=db, expenses=expenses, id_user = id_user)
    if expenses.remainders is not None:
        crud_remainders.create_remainders(db=db, remainders=expenses.remainders)
    return db_expenses

@router.get("/", response_model=LimitOffsetPage[schemas_expenses.ExpensesList])
async def get_expenses(skip: int = 0, limit: int = 25, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    expenses = crud_expenses.get_expenses(db, skip= skip, limit=limit, id_user = id_user)
    return paginate(expenses)
add_pagination(router)

@router.get("/{expenses_id}", response_model=schemas_expenses.ExpensesUpdate)
async def get_by_expenses(expenses_id: int, db: Session = Depends(get_db)):
    db_expenses = crud_expenses.get_by_expenses(db, expenses_id=expenses_id)
    if db_expenses is None:
        raise HTTPException(status_code=404, detail="Expenses Not found")
    return db_expenses

@router.delete("/{expenses_id}")
async def delete_expenses(expenses_id: int, db: Session = Depends(get_db)):
    db_expenses = crud_expenses.get_by_expenses(db, expenses_id=expenses_id)
    if db_expenses is None:
        raise HTTPException(status_code=404, detail="Expenses Not found")
    response = crud_expenses.delete_expenses(db=db,expenses_id=expenses_id)
    if response:
       message = "Delete Row" 
    else:
       message = "Error deleting Row"    
    return {"detail": message}

@router.put("/{expenses_id}",response_model=schemas_expenses.Expenses)
async def update_expenses(expenses_id: int, expenses: schemas_expenses.Expenses, db: Session = Depends(get_db)):
    db_expenses = crud_expenses.update_expenses(db, expenses_id=expenses_id, expenses = expenses)
    return db_expenses