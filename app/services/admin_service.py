from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User


def promote_user_to_admin(
    db: Session,
    user_id: int
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    # User does not exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # User is already an admin
    if user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already an admin"
        )

    # Promote user
    user.role = "admin"

    db.commit()
    db.refresh(user)

    return user