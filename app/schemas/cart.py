from pydantic import BaseModel, Field
from typing import List


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = {"from_attributes": True}


class CartRead(BaseModel):
    id: int
    items: List[CartItemRead] = []

    model_config = {"from_attributes": True}
