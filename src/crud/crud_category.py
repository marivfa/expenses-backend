from nis import cat
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, and_
from ..config.models import User, Category, CategoryBudget
from ..schema import schemas_category
from ..crud import crud_user


def get_by_category(db: Session, category_id: int, id_user: int = 0):
    return db.query(Category.id, Category.description, Category.id_user, Category.type, func.ifnull(CategoryBudget.budget, 0.00).label('budget'))\
        .outerjoin(CategoryBudget, and_(CategoryBudget.category_id == Category.id, CategoryBudget.user_id == id_user))\
        .filter(Category.id == category_id)\
        .first()

    return db.query(Expenses.id, Expenses.amount, Expenses.date_register, Expenses.id_category, Expenses.id_user, Category.description.label('category'), Expenses.comment, REAL_DATE)\
        .join(Category, Expenses.id_category == Category.id)\
        .filter(Expenses.id == expenses_id).first()


def get_category(db: Session, id_user: int = 0):
    filter_users = crud_user.get_related_users(db, id_user)
    filter_users.append(0)  # add default
    return db.query(Category.id, Category.type, Category.description, Category.id_user, func.ifnull(User.type, 'default').label('type_user'), func.ifnull(User.name, '').label('name_user'), func.ifnull(CategoryBudget.budget, 0.00).label('budget'))\
        .outerjoin(User, Category.id_user == User.id)\
        .outerjoin(CategoryBudget, and_(CategoryBudget.category_id == Category.id, CategoryBudget.user_id == id_user))\
        .filter(Category.id_user.in_(filter_users))\
        .all()


def create_category(db: Session, category: schemas_category.Category, id_user=int):
    db_category = Category(description=category.description,
                           type=category.type, id_user=id_user)
    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        inserted_id = db_category.id
        if category.budget > 0:
            db_budget = CategoryBudget(
                category_id=inserted_id, user_id=id_user, budget=category.budget)
            db.add(db_budget)
            db.commit()
    except:
        db.rollback()
        raise
    return db_category


def update_category(db: Session, category_id: int, category: schemas_category.Category, id_user=int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db_category.description = category.description
    db_category.type = category.type
    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        if category.budget > 0:
            db_budget = db.query(CategoryBudget).filter(
                CategoryBudget.category_id == category_id, CategoryBudget.user_id == id_user).first()
            if db_budget is None:
                db_budget = CategoryBudget(
                    category_id=category_id, user_id=id_user, budget=category.budget)
            else:
                db_budget.budget = category.budget
            db.add(db_budget)
            db.commit()
    except:
        db.rollback()
        raise
    return db_category


def delete_category(db: Session, category_id: int):
    row_count = db.query(Category).filter(Category.id == category_id).delete()
    db.commit()
    return row_count
