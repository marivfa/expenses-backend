from urllib import response
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from ..config.session import get_db
from ..crud import crud_remainders
from ..schema import schemas_remainders

from ..auth.auth import get_current_user

router = APIRouter(
    prefix="",
    tags=["remainders"]
)

# remainders


@router.post("/", status_code=201, response_model=schemas_remainders.Remainders)
async def create_remainders(remainders: schemas_remainders.Remainders, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    try:
        db_remainders = crud_remainders.create_remainders(
            db=db, remainders=remainders, id_user=id_user)
        return db_remainders
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid input data")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=LimitOffsetPage[schemas_remainders.RemaindersList])
async def get_remainders(skip: int = 0, limit: int = 25, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    reminders = crud_remainders.get_remainders(
        db, skip=skip, limit=limit, id_user=id_user)
    if reminders is None:
        raise HTTPException(status_code=404, detail="Reminder Not found")
    return paginate(reminders)
add_pagination(router)


@router.get("/detail/{reminders_id}")
async def get_reminders_detail(reminders_id: int, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    try:
        db_reminders = crud_remainders.get_reminders_detail(
            db, id_user=id_user, option='all', reminders_id=reminders_id)
        reminders = [{"description": e.description, "user": e.user, "date_time": e.date_time,
                      "status": e.status, "detail_id": e.detail_id} for e in db_reminders]
        return {"status": True, "data": reminders}
    except Exception as e:
        return {"status": False, "message": "Failed to retrieve reminders by date"}


@router.get("/{remainders_id}", response_model=schemas_remainders.Remainders)
async def get_by_remainders(remainders_id: int, db: Session = Depends(get_db)):
    db_remainders = crud_remainders.get_by_remainders(
        db, remainders_id=remainders_id)
    if db_remainders is None:
        raise HTTPException(status_code=404, detail="Reminder Not found")
    return db_remainders


@router.delete("/{remainders_id}")
async def delete_remainders(remainders_id: int, db: Session = Depends(get_db)):
    db_remainders = crud_remainders.get_by_remainders(
        db, remainders_id=remainders_id)
    if db_remainders is None:
        raise HTTPException(status_code=404, detail="Reminder Not found")
    if crud_remainders.delete_remainders(db=db, remainders_id=remainders_id):
        message = f"Row deleted successfully."
    else:
        message = f"Error deleting expenses row."
    return {"detail": message}


@router.put("/detail/{id}", response_model=schemas_remainders.RemindersDetail)
async def update_remainders(id: int, detail: schemas_remainders.RemindersDetailUpdate, db: Session = Depends(get_db)):
    db_detail = crud_remainders.update_remainders_detail(
        db, id=id, detail=detail)
    if db_detail is None:
        raise HTTPException(
            status_code=404, detail="Reminder detail Not found")
    return db_detail


@router.put("/{remainders_id}", response_model=schemas_remainders.Remainders)
async def update_remainders(remainders_id: int, remainder: schemas_remainders.Remainders, db: Session = Depends(get_db)):
    db_remainders = crud_remainders.update_remainders(
        db, remainders_id=remainders_id, remainder=remainder)
    if db_remainders is None:
        raise HTTPException(status_code=404, detail="Reminder Not found")
    return db_remainders
