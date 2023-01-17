from typing import List, Optional
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel

class RemaindersBase(BaseModel):
    class Config:
        orm_mode = True 

class FrecuencyEnum(str, Enum):
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'
    annual = 'annual'
    none = 'none'

class Remainders(RemaindersBase):
    description : str
    frecuency : FrecuencyEnum
    until_date : date
    id_user : int
    #remainder_date: date | None

class RemaindersList(RemaindersBase):
    id: int
    date_register : datetime
    description : str
    frecuency : FrecuencyEnum
    until_date : date
    #remainder_date: date | None
    id_user : int
