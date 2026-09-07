from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from typing import List

def create_order_from_items(db: Session, user_id: int, items: List[dict]) -> Order:
    """
    items: list of dicts {product_id, quantity, price}
    """
    total = 0.0
    order = Order(user_id=user_id, total_amount=0.0, status="pending")
    db.add(order)
    db.flush()  # get order.id

    for it in items:
        product = db.query(Product).filter(Product.id == it["product_id"]).with_for_update().one_or_none()
        if not product:
            raise ValueError(f"Product {it['product_id']} not found")
        if product.stock < it["quantity"]:
            raise ValueError(f"Insufficient stock for product {product.id}")
        product.stock -= it["quantity"]
        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=it["quantity"], price=it["price"])
        db.add(order_item)
        total += it["quantity"] * it["price"]

    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()
