from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_
from datetime import datetime

from ..config.models import Expenses, User, Category
from ..schema import schemas_expenses

from ..auth.auth import get_current_user

##Expenses
def get_by_expenses(db: Session, expenses_id: int):
    ##return db.query(Expenses).filter(Expenses.id == expenses_id).first()
    return db.query(Expenses.id,Expenses.amount, Expenses.date_register, Expenses.id_category, Expenses.id_user, Category.description.label('category'), Expenses.comment, Expenses.real_date)\
            .join(Category, Expenses.id_category == Category.id)\
            .filter(Expenses.id == expenses_id).first()

def get_expenses(db: Session, skip: int = 0, limit: int = 25, id_user: int = 0):
    return  db.query(Expenses.id,Expenses.amount, Expenses.date_register, Expenses.id_category, Expenses.real_date, Expenses.comment, Expenses.id_user, User.name.label('user'), Category.description.label('category'))\
            .join(User, Expenses.id_user == User.id)\
            .join(Category, Expenses.id_category == Category.id)\
            .filter(Expenses.id_user == id_user)\
            .order_by(Expenses.real_date.desc()).all() #.offset(skip).limit(limit)

def create_expenses(db: Session, expenses: schemas_expenses.Expenses, id_user = int):
    db_expenses = Expenses(amount = expenses.amount, real_date = expenses.real_date, comment = expenses.comment, id_category = expenses.id_category, id_user = id_user)
    db.add(db_expenses)
    db.commit()
    db.refresh(db_expenses)
    return db_expenses

def delete_expenses(db:Session, expenses_id: int):
    row_count = db.query(Expenses).filter(Expenses.id == expenses_id).delete()
    db.commit()
    return row_count

def update_expenses(db: Session, expenses_id: int, expenses: schemas_expenses.Expenses):
    db_expenses = db.query(Expenses).filter(Expenses.id == expenses_id).first()
    db_expenses.amount = expenses.amount
    db_expenses.id_category = expenses.id_category
    db.add(db_expenses)
    db.commit()
    db.refresh(db_expenses)
    return db_expenses


#Dashboard 
def get_expenses_monthly(db: Session, id_user: int):
    current_time = datetime.now()
    return db.query(func.ifnull(func.round(func.avg(Expenses.amount),2),0).label('average'), func.ifnull(func.round(func.sum(Expenses.amount),2),0).label('total'))\
        .filter(func.year(Expenses.real_date) == func.year(current_time), func.month(Expenses.real_date) == func.month(current_time), Expenses.id_user == id_user)\
        .first()

def get_total_expenses_annual(db: Session, id_user: int):
    current_time = datetime.now()
    return db.query(func.ifnull(func.sum(Expenses.amount),0).label('total'))\
        .filter(func.year(Expenses.real_date) == func.year(current_time), func.month(Expenses.real_date) == func.month(current_time), Expenses.id_user == id_user)\
        .first()

def get_expenses_by_category(db: Session, id_user: int):
    #current_time = datetime.now()
    return db.query(Category.description.label('category'), func.ifnull(func.sum(Expenses.amount),0).label('amount'))\
           .join(Category, Expenses.id_category == Category.id)\
           .filter(Expenses.id_user == id_user)\
           .group_by(Category.id)\
           .order_by(Expenses.amount.desc())

def get_expenses_by_type(db: Session,id_user: int):
    #current_time = datetime.now()
    return db.query(Category.type, func.ifnull(func.sum(Expenses.amount),0).label('amount'))\
           .join(Category, Expenses.id_category == Category.id)\
           .filter(Expenses.id_user == id_user)\
           .group_by(Category.type)

def get_expenses_by_month(db: Session,id_user: int):
    #current_time = datetime.now()
    return db.query((func.year(Expenses.real_date) +"-"+ func.month(Expenses.real_date)).label('Date'), func.ifnull(func.sum(Expenses.amount),0).label('amount'))\
           .filter(Expenses.id_user == id_user)\
           .group_by(func.year(Expenses.real_date),func.month(Expenses.real_date)).all()