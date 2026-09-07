from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, payload: ProductCreate) -> Product:
    p = Product(**payload.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db: Session, q: Optional[str] = None, category_id: Optional[int] = None,
                  min_price: Optional[float] = None, max_price: Optional[float] = None,
                  limit: int = 20, offset: int = 0) -> List[Product]:
    qry = db.query(Product)
    if q:
        qry = qry.filter(Product.name.ilike(f"%{q}%"))
    if category_id:
        qry = qry.filter(Product.category_id == category_id)
    if min_price is not None:
        qry = qry.filter(Product.price >= min_price)
    if max_price is not None:
        qry = qry.filter(Product.price <= max_price)
    return qry.offset(offset).limit(limit).all()

def update_product(db: Session, product_id: int, payload: ProductUpdate):
    product = get_product(db, product_id)
    if not product:
        return None
    for key, val in payload.dict(exclude_unset=True).items():
        setattr(product, key, val)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product
