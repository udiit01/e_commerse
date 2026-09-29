from pydantic import BaseModel,Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float=Field(ge=0)
    category_id: int
    stock: int =  Field(default=0, ge=0)


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category_id: Optional[int]
    stock: Optional[int]

class ProductRead(ProductBase):
    id: int
    class Config:
        from_attributes = True




        