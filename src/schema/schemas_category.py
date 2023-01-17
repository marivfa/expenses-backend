from typing import List, Optional
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel


class CategoryBase(BaseModel):
    class Config:
        orm_mode = True

class TypeCatEnum(str, Enum):
    fixed = 'fixed'
    flex = 'flex'
    none = 'None'

class Category(CategoryBase):
    description : str      
    type : TypeCatEnum

class CategoryList(CategoryBase):
    id: int
    description : str      
    type : TypeCatEnum
