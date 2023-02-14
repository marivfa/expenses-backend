from enum import Enum
from pydantic import BaseModel


class CategoryBase(BaseModel):
    class Config:
        orm_mode = True

class TypeCatEnum(str, Enum):
    fixed = 'fixed'
    flex = 'flex'
    other = 'other'

class Category(CategoryBase):
    description : str      
    type : TypeCatEnum
    id_user : int

class CategoryList(CategoryBase):
    id: int
    description : str      
    type : TypeCatEnum
    id_user : int
    type_user : str | None
    name_user : str | None