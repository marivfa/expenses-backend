from typing import List, Optional
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel

class UserBase(BaseModel):
    class Config:
        orm_mode = True

class ActiveEnum(str, Enum):
    Y = 'Y'
    N = 'N'

class TypeEnum(str, Enum):
    admin = 'admin'
    delegate = 'delegate'

class User(UserBase):
    id : int | None
    name : str
    email : str
    active : ActiveEnum
    type : TypeEnum
    master_id : int
    country : str | None
    currency : str | None
    password : str | None


class UserUpdate(UserBase):
    country : str | None
    currency : str | None
    # name : str | None
    # active : ActiveEnum

