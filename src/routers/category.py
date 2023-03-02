from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from ..config.session import get_db
from ..crud import crud_category
from ..schema import schemas_category

from ..auth.auth import get_current_user

router = APIRouter(
    prefix="",
    tags=["category"]
)

# Category


@router.post("/", status_code=201, response_model=schemas_category.Category)
async def create_category(category: schemas_category.Category, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    try:
        db_category = crud_category.create_category(
            db=db, category=category, id_user=id_user)
        return db_category
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid input data")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[schemas_category.CategoryList])
async def get_category(db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    db_category = crud_category.get_category(db, id_user=id_user)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category Not found")
    return db_category


@router.get("/{category_id}", response_model=schemas_category.Category)
async def get_by_category(category_id: int, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    db_category = crud_category.get_by_category(
        db, category_id=category_id,  id_user=id_user)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category Not found")
    return db_category


@router.put("/{category_id}", response_model=schemas_category.Category)
async def update_category(category_id: int, category: schemas_category.Category, db: Session = Depends(get_db), id_user: int = Depends(get_current_user)):
    try:
        db_category = crud_category.update_category(
            db, category_id=category_id, category=category, id_user=id_user)
        return db_category
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Invalid input data")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.get_by_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category Not found")
    if crud_category.delete_category(db=db, category_id=category_id):
        message = f"Row with category_id {category_id} deleted successfully."
    else:
        message = f"Error deleting row with category_id {category_id}."
    return {"detail": message}
