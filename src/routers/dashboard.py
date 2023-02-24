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
    response = {"avg_monthly": 0, "total_annual": 0, "count_remainders":0,"expenses_monthly":0, "count_expenses":0}
    db_exp_monthly = crud_expenses.get_expenses_monthly(db, id_user)
    db_exp_avg = crud_expenses.get_expenses_avg(db,id_user)
    db_exp_total = crud_expenses.get_total_expenses_annual(db,id_user)
    db_rem_count = crud_remainders.count_remainders(db,id_user)
    db_exp_count = crud_expenses.count_expenses(db, id_user)
    if db_exp_avg: 
        response.update({"avg_monthly": db_exp_avg.average})
    if db_exp_monthly:
        response.update({"expenses_monthly": db_exp_monthly.total})
    if db_exp_total:
        response.update({"total_annual": db_exp_total.total})
    if db_rem_count:
        response.update({"count_remainders": db_rem_count})
    if db_exp_count:
        response.update({"count_expenses": db_exp_count})
    return response

@router.get("/by_month")
async def get_expenses_by_month(db: Session = Depends(get_db),id_user: int = Depends(get_current_user)):
    try:
        db_expenses = crud_expenses.get_expenses_by_month(db,id_user)
        expenses = [{"date": e.date, "amount": e.amount} for e in db_expenses]
        return {"status": True, "data": expenses}
    except Exception as e:
        print(f"Failed to retrieve expenses: {e}")
        return {"status": False, "message": "Failed to retrieve expenses by month"}

@router.get("/by_category")
async def get_expenses_by_category(db: Session = Depends(get_db),id_user: int = Depends(get_current_user)):
    try:
        db_expenses = crud_expenses.get_expenses_by_category(db,id_user)
        expenses = [{"category": e[0], "amount": e[1]} for e in db_expenses]
        return {"status": True, "data": expenses}
    except Exception as e:
        print(f"Failed to retrieve expenses: {e}")
        return {"status": False, "message": "Failed to retrieve expenses by category"}


@router.get("/by_type")
async def get_expenses_by_type(db: Session = Depends(get_db),id_user: int = Depends(get_current_user)):
    try:
        db_expenses = crud_expenses.get_expenses_by_type(db,id_user)
        expenses = [{"type": e[0], "value": e[1]} for e in db_expenses]
        return {"status": True, "data": expenses}
    except Exception as e:
        print(f"Failed to retrieve expenses: {e}")
        return {"status": False, "message": "Failed to retrieve expenses by type"}
    

@router.get("/reminder")
async def get_reminders_by_date(option: str = 'day', db: Session = Depends(get_db),id_user: int = Depends(get_current_user)):
    try:
        db_reminders = crud_remainders.get_reminders_detail(db,id_user, option=option)
        reminders = [{"description": e.description, "user": e.user, "date_time": e.date_time, "status": e.status, "detail_id" : e.detail_id} for e in db_reminders]
        return {"status": True, "data": reminders}
    except Exception as e:
        print(f"Failed to retrieve reminders: {e}")
        return {"status": False, "message": "Failed to retrieve reminders by date"}

