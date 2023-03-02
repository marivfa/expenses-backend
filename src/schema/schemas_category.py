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
    description: str
    type: TypeCatEnum
    id_user: int | None

    budget: float | None


class CategoryList(CategoryBase):
    id: int
    description: str
    type: TypeCatEnum
    id_user: int
    type_user: str | None
    name_user: str | None

    budget: float | None


class CategoryBudgetBase(BaseModel):
    class Config:
        orm_mode = True


class CategoryBudget(CategoryBudgetBase):
    id: int
    category_id: int
    user_id: int
    budget: float


class CategoryBudgetUpdate(CategoryBudgetBase):
    budget: float
