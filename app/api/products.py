from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.product_service import create_product, get_product, list_products, update_product, delete_product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.core.security import require_admin
from app.models.user import User

router = APIRouter(prefix="/products", tags=["Products"])



# Public: Anyone can view products
@router.get("/", response_model=list[ProductRead])
def search(
    q: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return list_products(
        db,
        q=q,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        limit=limit,
        offset=offset
    )


# Public: Anyone can view a single product
@router.get("/{product_id}", response_model=ProductRead)
def read(
    product_id: int,
    db: Session = Depends(get_db)
):
    p = get_product(db, product_id)

    if not p:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return p


# Admin only: Create product
@router.post("/", response_model=ProductRead)
def create(
    p: ProductCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return create_product(db, p)


# Admin only: Update product
@router.put("/{product_id}", response_model=ProductRead)
def update(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    p = update_product(db, product_id, payload)

    if not p:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return p


# Admin only: Delete product
@router.delete("/{product_id}")
def remove(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    p = delete_product(db, product_id)

    if not p:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {"detail": "deleted"}