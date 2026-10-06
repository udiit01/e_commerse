from pydantic import BaseModel,Field
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )
    parent_id: Optional[int] = None
    

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    subcategories: List["CategoryRead"] = []
    class Config:
        from_attributes = True


        