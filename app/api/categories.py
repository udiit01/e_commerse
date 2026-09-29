from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_admin
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate
router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/")
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
      # 1. Check duplicate category
    existing_category = (
        db.query(Category)
        .filter(Category.name == payload.name)
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"

        )
       # 2. Check parent category
    if payload.parent_id is not None:
        parent_category = (
            db.query(Category)
            .filter(Category.id == payload.parent_id)
            .first()
        )

        if not parent_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent category not found"
            )

    # 3. Create category
    category = Category(
        name=payload.name,
        parent_id=payload.parent_id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get("/")
def list_categories(
    db: Session = Depends(get_db)
):
    return db.query(Category).all()