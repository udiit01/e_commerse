from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.product import Product


def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = (
        db.query(Cart)
        .filter(Cart.user_id == user_id)
        .first()
    )

    if cart:
        return cart

    cart = Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart


def add_item_to_cart(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int = 1
):
    # Check whether product exists
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Get user's cart
    cart = get_or_create_cart(db, user_id)

    # Check whether product already exists in cart
    item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
        .first()
    )

    # Calculate final quantity
    if item:
        final_quantity = item.quantity + quantity
    else:
        final_quantity = quantity

    # Check stock
    if final_quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} items are available in stock"
        )

    # Update existing item
    if item:
        item.quantity = final_quantity

    # Create new item
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(item)

    db.commit()
    db.refresh(item)

    return item


def remove_item_from_cart(
    db: Session,
    user_id: int,
    cart_item_id: int
):
    cart = get_or_create_cart(db, user_id)

    item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.id == cart_item_id
        )
        .first()
    )

    if not item:
        return None

    db.delete(item)
    db.commit()

    return True


def clear_cart(
    db: Session,
    user_id: int
):
    cart = get_or_create_cart(db, user_id)

    for item in list(cart.items):
        db.delete(item)

    db.commit()

    return True



def update_cart_item(
    db: Session,
    user_id: int,
    cart_item_id: int,
    quantity: int
):
    cart = get_or_create_cart(db, user_id)

    item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.id == cart_item_id
        )
        .first()
    )

    if not item:
        return None

    product = (
        db.query(Product)
        .filter(Product.id == item.product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock} items are available in stock"
        )

    item.quantity = quantity

    db.commit()
    db.refresh(item)

    return item
