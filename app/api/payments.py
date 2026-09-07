from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.payment_service import capture_payment

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/capture/{payment_id}")
def capture(payment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = capture_payment(db, payment_id)
    if not p:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"id": p.id, "status": p.status}
