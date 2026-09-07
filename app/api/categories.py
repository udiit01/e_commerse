from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.category import Category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/")
def create_category(name: str, parent_id: int | None = None, db: Session = Depends(get_db)):
    category = Category(name=name, parent_id=parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
