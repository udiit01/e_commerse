from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.cart_service import add_item_to_cart, get_or_create_cart, remove_item_from_cart, clear_cart, update_cart_item
from app.schemas.cart import CartItemCreate, CartRead ,  CartItemUpdate
from app.core.security import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

print(">>> LOADING PUT CART UPDATE ROUTE")
@router.put("/items/{cart_item_id}")
def update_item(
    cart_item_id: int,
    payload: CartItemUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    item = update_cart_item(
        db,
        user.id,
        cart_item_id,
        payload.quantity
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {
        "id": item.id,
        "product_id": item.product_id,
        "quantity": item.quantity
    }

@router.post("/items", response_model=dict)
def add_item(payload: CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = add_item_to_cart(db, user.id, payload.product_id, payload.quantity)
    return {"id": item.id, "product_id": item.product_id, "quantity": item.quantity}

@router.get("/", response_model=CartRead)
def get_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart = get_or_create_cart(db, user.id)
    return cart

@router.delete("/items/{cart_item_id}")
def remove_item(cart_item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ok = remove_item_from_cart(db, user.id, cart_item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "removed"}

@router.delete("/")
def empty_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    clear_cart(db, user.id)
    return {"detail": "cart cleared"}
