from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, Enum, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, index=True)
    active = Column('active',Enum("Y", "N"), default="Y")
    type = Column('type',Enum("admin", "delegate"), default="admin")
    master_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    country = Column(String(10))
    currency = Column(String(10))

    children = relationship("User", backref="parent", remote_side=[id])
    expenses = relationship("Expenses",back_populates="user_name")

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100))       
    type = Column(Enum("fixed", "flex","other"),default="other")   

    id_user = Column(Integer, ForeignKey("users.id"))
    expenses = relationship("Expenses",back_populates="category_name")

class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    date_register = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(DECIMAL(10,2))
    real_date = Column(Date)
    comment = Column(String(200))

    id_user = Column(Integer, ForeignKey("users.id"))
    id_category = Column(Integer, ForeignKey("category.id"))

    user_name = relationship("User",back_populates="expenses")
    category_name = relationship("Category",back_populates="expenses")

class Remainders(Base):
    __tablename__ = "remainders"
    id = Column(Integer, primary_key=True, index=True)
    date_register = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String(100))
    frecuency = Column(Enum("daily", "weekly","monthly","annual","none"),default="none")   
    until_date = Column(Date)
    id_user = Column(Integer, ForeignKey("users.id"))
    remainder_date = Column(Date)

class RemindersDetail(Base):
    __tablename__ = "reminders_detail"
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(Date, server_default=func.now())
    status = Column(String(100))
    reminder_id = Column(Integer, ForeignKey("remainders.id"))