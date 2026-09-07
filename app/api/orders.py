from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.order_service import create_order_from_items, get_order
from app.services.payment_service import initiate_payment
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderRead)
def place_order(payload: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # simple flow:
    try:
        # convert items to simple dicts usable by service
        items = [{"product_id": it.product_id, "quantity": it.quantity, "price": it.price} for it in payload.items]
        order = create_order_from_items(db, user.id, items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # initiate payment (stub)
    payment = initiate_payment(db, order.id, order.total_amount)
    # in real flow redirect to provider or return client secret
    return order

@router.get("/{order_id}", response_model=OrderRead)
def get_one(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    o = get_order(db, order_id)
    if not o or o.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return o
