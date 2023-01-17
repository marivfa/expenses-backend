from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..config.session import get_db
from ..crud import crud_category
from ..schema import schemas_category

router = APIRouter(
    prefix="",
    tags=["category"]
)


##Category 
@router.post("/", status_code=201 ,response_model=schemas_category.Category)
async def create_category(category: schemas_category.Category, db: Session = Depends(get_db)):
    db_category = crud_category.create_category(db=db, category=category)
    return db_category

@router.get("/", response_model=List[schemas_category.CategoryList])
async def get_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    category = crud_category.get_category(db, skip= skip, limit=limit)
    return category

@router.get("/{category_id}", response_model=schemas_category.Category)
async def get_by_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.get_by_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category Not found")
    return db_category

@router.put("/{category_id}",response_model=schemas_category.Category)
async def update_category(category_id: int, category: schemas_category.Category, db: Session = Depends(get_db)):
    db_category = crud_category.update_category(db, category_id=category_id, category = category)
    return db_category

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.get_by_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category Not found")
    response = crud_category.delete_category(db=db,category_id=category_id)
    if response:
       message = "Delete Row" 
    else:
       message = "Error deleting Row"    
    return {"detail": message}