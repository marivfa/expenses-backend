from sqlalchemy.orm import Session
from sqlalchemy.sql import func, text
from sqlalchemy import and_
from typing import List, Tuple
from datetime import datetime

from ..config.models import Expenses, User, Category
from ..schema import schemas_expenses
from ..crud import crud_user

# Expenses
YEAR = func.year(Expenses.real_date)
MONTH = func.month(Expenses.real_date)
current_time = datetime.now()


def get_by_expenses(db: Session, expenses_id: int):
    # return db.query(Expenses).filter(Expenses.id == expenses_id).first()
    return db.query(Expenses.id, Expenses.amount, Expenses.date_register, Expenses.id_category, Expenses.id_user, Category.description.label('category'), Expenses.comment, Expenses.real_date)\
        .join(Category, Expenses.id_category == Category.id)\
        .filter(Expenses.id == expenses_id).first()


def get_expenses(db: Session, skip: int = 0, limit: int = 25, id_user: int = 0, download: str = ''):
    filter_users = crud_user.get_related_users(db, id_user)
    if download == 'xls':
        return db.query(User.name.label('User'), Category.description.label('Category'), Expenses.amount, Expenses.comment, Expenses.date_register, Expenses.real_date)\
            .join(User, Expenses.id_user == User.id)\
            .join(Category, Expenses.id_category == Category.id)\
            .filter(Expenses.id_user.in_(filter_users))\
            .order_by(Expenses.real_date.desc()).all()
    else:
        return db.query(Expenses.id, Expenses.amount, Expenses.date_register, Expenses.id_category, Expenses.real_date, Expenses.comment, Expenses.id_user, User.type, User.name.label('user'), Category.description.label('category'))\
            .join(User, Expenses.id_user == User.id)\
            .join(Category, Expenses.id_category == Category.id)\
            .filter(Expenses.id_user.in_(filter_users))\
            .order_by(Expenses.real_date.desc()).all()


def create_expenses(db: Session, expenses: schemas_expenses.Expenses, id_user=int):
    db_expenses = Expenses(amount=expenses.amount, real_date=expenses.real_date,
                           comment=expenses.comment, id_category=expenses.id_category, id_user=id_user)
    db.add(db_expenses)
    db.commit()
    db.refresh(db_expenses)
    return db_expenses


def delete_expenses(db: Session, expenses_id: int):
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


# Dashboard
def get_expenses_monthly(db: Session, id_user: int):
    filter_users = crud_user.get_related_users(db, id_user)
    return db.query(func.ifnull(func.round(func.sum(Expenses.amount), 2), 0).label('total'))\
        .filter(YEAR == func.year(current_time), MONTH == func.month(current_time), Expenses.id_user.in_(filter_users))\
        .first()

def get_expenses_avg(db: Session, id_user: int):
    filter_users = crud_user.get_related_users(db, id_user)
    return db.query(func.ifnull(func.round(func.avg(Expenses.amount), 2), 0).label('average'))\
        .filter(YEAR == func.year(current_time), Expenses.id_user.in_(filter_users))\
        .first()

def get_total_expenses_annual(db: Session, id_user: int):
    filter_users = crud_user.get_related_users(db, id_user)
    return db.query(func.ifnull(func.sum(Expenses.amount), 0).label('total'))\
        .filter(YEAR == func.year(current_time), Expenses.id_user.in_(filter_users))\
        .first()


def get_expenses_by_category(db: Session, id_user: int):
    filter_users = crud_user.get_related_users(db, id_user)
    try:
        return db.query(Category.description.label('category'), func.ifnull(func.sum(Expenses.amount), 0).label('amount'))\
            .join(Category, Expenses.id_category == Category.id)\
            .filter(Expenses.id_user.in_(filter_users))\
            .group_by(Category.id)\
            .order_by(Expenses.amount.desc())
    except Exception as e:
        print(f"Failed to retrieve expenses by category: {e}")
        return []


def get_expenses_by_type(db: Session, id_user: int):
    filter_users = crud_user.get_related_users(db, id_user)
    try:
        return db.query(Category.type, func.ifnull(func.sum(Expenses.amount), 0).label('amount'))\
            .join(Category, Expenses.id_category == Category.id)\
            .filter(Expenses.id_user.in_(filter_users))\
            .group_by(Category.type)
    except Exception as e:
        print(f"Failed to retrieve expenses by type: {e}")
        return []


def get_expenses_by_month(db: Session, id_user: int):
    filter_users = crud_user.get_related_users(db, id_user)
    try:
        return db.query((func.year(Expenses.real_date) +"-"+ func.month(Expenses.real_date)).label('date'), YEAR.label('Year'), MONTH.label('Month'), func.ifnull(func.sum(Expenses.amount),0).label('amount'))\
            .filter(Expenses.id_user.in_(filter_users))\
            .group_by('Year','Month').all()
    except Exception as e:
        print(f"Failed to retrieve expenses: {e}")
        return []