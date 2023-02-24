from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import pandas as pd
import os

from ..config.session import get_db
from ..crud import crud_expenses, crud_remainders
from ..schema import schemas_expenses

from dotenv import load_dotenv

from ..auth.auth import get_current_user, aws_session

load_dotenv()

router = APIRouter(
    prefix="",
    tags=["expenses"]
)


##Expenses
@router.post("/", status_code=201 ,response_model=schemas_expenses.Expenses)
async def create_expenses(expenses: schemas_expenses.Expenses, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    try:
        db_expenses = crud_expenses.create_expenses(db=db, expenses=expenses, id_user = id_user)
        if expenses.remainders is not None:
            crud_remainders.create_remainders(db=db, remainders=expenses.remainders)
        return db_expenses
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid input data")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    
@router.get("/", response_model=LimitOffsetPage[schemas_expenses.ExpensesList])
async def get_expenses(skip: int = 0, limit: int = 25, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    expenses = crud_expenses.get_expenses(db, skip= skip, limit=limit, id_user = id_user)
    if expenses is None:
        raise HTTPException(status_code=404, detail="Reminder Not found")
    return paginate(expenses)
add_pagination(router)

@router.get("/xls")
async def get_data_excel(db: Session = Depends(get_db), id_user: str = Depends(get_current_user)):
    expenses = crud_expenses.get_expenses(db, 0, 0,id_user = id_user, download = 'xls')
    df = pd.DataFrame(
        expenses, 
        columns=["User","Category","Amount","Comment","Date register","Real date"]
    )

    file_name = f"data{id_user}.csv"
    df.to_csv(file_name, index=False)

    session = aws_session() 
    s3_resource = session.client('s3')

    try:
        s3_resource.upload_file(file_name,os.environ.get('S3_NAME'),f"public/{file_name}")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Error uploading file: "+str(e))

    return {'url': f"{file_name}"} 

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