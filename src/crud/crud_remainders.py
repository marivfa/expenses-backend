from sqlalchemy.orm import Session
from sqlalchemy.sql import func, and_
from datetime import datetime

from ..config.models import Remainders, User
from ..schema import schemas_remainders

from ..auth.auth import get_current_user

##Remainders
def get_by_remainders(db: Session, remainders_id: int):
    return db.query(Remainders).filter(Remainders.id == remainders_id).first()

def get_remainders(db: Session, skip: int = 0, limit: int = 100, id_user = int):
    return db.query(Remainders.id, Remainders.date_register, Remainders.description, Remainders.frecuency, Remainders.until_date, Remainders.id_user, User.name.label('user'))\
           .join(User, Remainders.id_user == User.id)\
           .filter(Remainders.id_user == id_user)\
           .all()

def create_remainders(db: Session, remainders: schemas_remainders.Remainders, id_user = int):
    remainders.id_user = id_user
    db_remainders = Remainders(**remainders.dict())
    db.add(db_remainders)
    db.commit()
    db.refresh(db_remainders)
    return db_remainders

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
def count_remainders(db:Session,id_user: int):
    current_time = datetime.now()
    return db.query(Remainders).filter(and_(current_time < Remainders.until_date)).count()
