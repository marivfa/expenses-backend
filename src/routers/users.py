from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from ..config.session import get_db
from ..crud import crud_user
from ..schema import schemas_user

from ..auth.auth import get_current_user

router = APIRouter(
    prefix="",
    tags=["users"]
)


@router.post("/", status_code=201, response_model=schemas_user.User)
async def create_user(user: schemas_user.User, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email alredy exist")
    return crud_user.create_user(db=db, user=user, user_id=user_id)


@router.get("/", response_model=List[schemas_user.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=schemas_user.User)
async def get_profile(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    db_user = crud_user.get_by_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    return db_user


@router.get("/{user_id}", response_model=schemas_user.User)
async def get_by_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_by_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    return db_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_by_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    if crud_user.delete_user(db=db, user_id=user_id):
        message = f"Row deleted successfully."
    else:
        message = f"Error deleting expenses row."
    return {"detail": message}


@router.put("/me", response_model=schemas_user.User)
async def update_user(user: schemas_user.UserUpdate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        db_users = crud_user.update_user(db, users=user, user_id=user_id)
        return db_users
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid input data")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
