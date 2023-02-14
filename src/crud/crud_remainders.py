from sqlalchemy.orm import Session
from sqlalchemy.sql import func, and_
from datetime import date, datetime, timedelta

from ..config.models import Remainders, RemindersDetail, User
from ..schema import schemas_remainders
from ..crud import crud_user

from ..auth.auth import get_current_user

##Remainders
def get_by_remainders(db: Session, remainders_id: int):
    return db.query(Remainders).filter(Remainders.id == remainders_id).first()

def get_remainders(db: Session, skip: int = 0, limit: int = 100, id_user = int):
    filter_users = crud_user.get_related_users(db, id_user)
    return db.query(Remainders.id, Remainders.date_register, Remainders.description, Remainders.frecuency, Remainders.until_date, Remainders.remainder_date, Remainders.id_user, User.name.label('user'))\
           .join(User, Remainders.id_user == User.id)\
           .filter(Remainders.id_user.in_(filter_users))\
           .all()

def create_remainders(db: Session, remainders: schemas_remainders.Remainders, id_user = int):
    try:
        remainders.id_user = id_user
        db_remainders = Remainders(**remainders.dict())
        db.add(db_remainders)
        db.commit()
        db.refresh(db_remainders)
        inserted_id = db_remainders.id

        if remainders.frecuency != 'none':
            details = generate_details(remainders.remainder_date, remainders.until_date, remainders.frecuency, inserted_id)
            for detail in details:
                db.add(detail)
        db.commit()
    except:
        db.rollback()
        raise

    return db_remainders

def generate_details(start_date, end_date, frequency, reminder_id):
    details = []
    current_date = start_date
    while current_date <= end_date:
        details.append(RemindersDetail(reminder_id=reminder_id, date_time=current_date, status='pending'))
        if frequency == 'daily':
            current_date += timedelta(days=1)
        elif frequency == 'weekly':
            current_date += timedelta(weeks=1)
        elif frequency == 'monthly':
            current_month = current_date.month
            current_year = current_date.year
            if current_month == 12:
                current_month = 1
                current_year += 1
            else:
                current_month += 1
            current_date = date(current_year, current_month, current_date.day)
    return details

def delete_remainders(db:Session, remainders_id: int):
    row_count = db.query(Remainders).filter(Remainders.id == remainders_id).delete()
    db.commit()
    return row_count

def update_remainders(db: Session, remainders_id: int, remainder: schemas_remainders.Remainders):
    db_remainder = db.query(Remainders).filter(Remainders.id == remainders_id).first()
    db_remainder.description = remainder.description
    db_remainder.frecuency = remainder.frecuency
    db_remainder.until_date = remainder.until_date
    db.add(db_remainder)
    db.commit()
    db.refresh(db_remainder)
    return db_remainder

#Dashboard
def get_reminders_detail(db: Session, id_user = int, option = str):
    current_time = datetime.now().date()
    current_week_start = current_time - timedelta(days=current_time.weekday())
    current_week_end = current_week_start + timedelta(days=6)

    MONTH = func.month(RemindersDetail.date_time)
    YEAR = func.year(RemindersDetail.date_time)

    filter_users = crud_user.get_related_users(db, id_user)

    if option == 'daily':
        return db.query(Remainders.id, Remainders.description, Remainders.frecuency, Remainders.id_user, User.name.label('user'), RemindersDetail.id.label('detail_id'), RemindersDetail.date_time, RemindersDetail.status)\
            .outerjoin(RemindersDetail, Remainders.id == RemindersDetail.reminder_id)\
            .join(User, Remainders.id_user == User.id)\
            .filter(func.date(RemindersDetail.date_time) == func.date(current_time), Remainders.id_user.in_(filter_users))\
            .all()
    elif option == 'weekly':
        return db.query(Remainders.id, Remainders.description, Remainders.frecuency, Remainders.id_user, User.name.label('user'), RemindersDetail.id.label('detail_id') ,RemindersDetail.date_time, RemindersDetail.status)\
            .outerjoin(RemindersDetail, Remainders.id == RemindersDetail.reminder_id)\
            .join(User, Remainders.id_user == User.id)\
            .filter(func.date(RemindersDetail.date_time) >= func.date(current_week_start), func.date(RemindersDetail.date_time) <= func.date(current_week_end), Remainders.id_user.in_(filter_users))\
            .all()
    elif option == 'monthly':
        return db.query(Remainders.id, Remainders.description, Remainders.frecuency, Remainders.id_user, User.name.label('user'), RemindersDetail.id.label('detail_id') ,RemindersDetail.date_time, RemindersDetail.status)\
            .outerjoin(RemindersDetail, Remainders.id == RemindersDetail.reminder_id)\
            .join(User, Remainders.id_user == User.id)\
            .filter(YEAR == func.year(current_time), MONTH == func.month(current_time), Remainders.id_user.in_(filter_users))\
            .all()

    

def count_remainders(db:Session,id_user: int):
    current_time = datetime.now()
    return db.query(Remainders).filter(and_(current_time < Remainders.until_date)).count()
