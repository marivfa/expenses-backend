from sqlalchemy.orm import Session

from ..config import models
from ..schema import schemas_category

def get_by_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas_category.Category):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas_category.Category):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    db_category.description = category.description
    db_category.type = category.type
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db:Session, category_id: int):
    row_count = db.query(models.Category).filter(models.Category.id == category_id).delete()
    db.commit()
    return row_count