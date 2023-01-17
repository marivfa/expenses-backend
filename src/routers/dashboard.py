from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..config.session import get_db
from ..crud import crud_remainders, crud_expenses

from ..auth.auth import get_current_user

router = APIRouter(
    prefix="",
    tags=["dashboard"]
)

@router.get("/resumen")
async def get_expenses_resume(db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    response = {"avg_monthly": 0, "total_annual": 0, "count_remainders":0,"expenses_monthly":0}
    db_exp_monthly = crud_expenses.get_expenses_monthly(db, id_user)
    db_exp_total = crud_expenses.get_total_expenses_annual(db,id_user)
    db_rem_count = crud_remainders.count_remainders(db,id_user)
    if db_exp_monthly:
        response.update({"avg_monthly": db_exp_monthly.average,"expenses_monthly": db_exp_monthly.total})
    if db_exp_total:
        response.update({"total_annual": db_exp_total.total})
    if db_rem_count:
        response.update({"count_remainders": db_rem_count})
    return response

@router.get("/by_month")
async def get_expenses_by_month(db: Session = Depends(get_db),id_user: int = Depends(get_current_user)):
    db_expenses = crud_expenses.get_expenses_by_month(db,id_user)
    return db_expenses

@router.get("/by_category")
async def get_expenses_by_category(db: Session = Depends(get_db),id_user: int = Depends(get_current_user)):
    db_expenses = crud_expenses.get_expenses_by_category(db,id_user)
    return db_expenses

@router.get("/by_type")
async def get_expenses_by_type(db: Session = Depends(get_db),id_user: int = Depends(get_current_user)):
    db_expenses = crud_expenses.get_expenses_by_type(db,id_user)
    return db_expenses