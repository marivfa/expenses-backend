from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from ..config.models import User, Category
from ..schema import schemas_category
from ..crud import crud_user

def get_by_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_category(db: Session, id_user: int = 0):
    filter_users = crud_user.get_related_users(db, id_user)
    filter_users.append(0) #add default
    return db.query(Category.id, Category.type, Category.description, Category.id_user, func.ifnull(User.type, 'default').label('type_user'), func.ifnull(User.name,'').label('name_user'))\
           .outerjoin(User, Category.id_user == User.id)\
           .filter(Category.id_user.in_(filter_users))\
           .all()

def create_category(db: Session, category: schemas_category.Category, id_user = int):
    db_category = Category(**category.dict())
    db_category.id_user = id_user
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas_category.Category):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db_category.description = category.description
    db_category.type = category.type
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db:Session, category_id: int):
    row_count = db.query(Category).filter(Category.id == category_id).delete()
    db.commit()
    return row_count