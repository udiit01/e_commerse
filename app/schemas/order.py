from pydantic import BaseModel
from typing import List, Optional

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItem]

class OrderRead(BaseModel):
    id: int
    total_amount: float
    status: str
    class Config:
        orm_mode = True
