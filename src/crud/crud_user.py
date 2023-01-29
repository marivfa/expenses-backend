from sqlalchemy.orm import Session

from ..config import models
from ..schema import schemas_user

import boto3

def get_by_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas_user.User, user_id = int):
    if user.type == 'delegate':
        user.master_id = user_id
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email = str):
    return db.query(models.User).filter(models.User.email == email).first()
    
def delete_user(db:Session, user_id: int):
    row_count = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return row_count

def update_user(db: Session, users: schemas_user.UserUpdate,user_id = int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    #db_user.name = users.name
    db_user.country = users.country
    db_user.currency = users.currency
    db_user.id = user_id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_cognito_user():
    ##client = boto3.client('cognito-idp')
    pass
    