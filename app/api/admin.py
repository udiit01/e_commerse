from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_admin
from app.models.user import User

from app.services.admin_service import (
    promote_user_to_admin
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/users/{user_id}/promote")
def promote_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    user = promote_user_to_admin(
        db,
        user_id
    )

    return {
        "message": "User promoted to admin successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }