from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.product import Product

def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if cart:
        return cart
    cart = Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

def add_item_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1):
    cart = get_or_create_cart(db, user_id)
    item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_item_from_cart(db: Session, user_id: int, cart_item_id: int):
    cart = get_or_create_cart(db, user_id)
    item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.id == cart_item_id).first()
    if not item:
        return None
    db.delete(item)
    db.commit()
    return True

def clear_cart(db: Session, user_id: int):
    cart = get_or_create_cart(db, user_id)
    for item in list(cart.items):
        db.delete(item)
    db.commit()
    return True
