from pydantic import BaseModel
from typing import List

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    class Config:
        orm_mode = True

class CartRead(BaseModel):
    id: int
    items: List[CartItemRead] = []
    class Config:
        orm_mode = True
