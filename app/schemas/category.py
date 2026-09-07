from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    subcategories: List["CategoryRead"] = []
    class Config:
        orm_mode = True