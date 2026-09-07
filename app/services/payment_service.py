from typing import Dict
from app.models.payment import Payment
from sqlalchemy.orm import Session

class PaymentProviderStub:
    """
    Replace with real Stripe/PayPal SDK integration.
    This stub just simulates a provider response.
    """
    def create_payment(self, amount: float, currency: str = "usd") -> Dict:
        # create a fake provider id
        return {"id": f"prov_{int(amount*100)}", "status": "created", "amount": amount, "currency": currency}

    def capture_payment(self, provider_payment_id: str) -> Dict:
        return {"id": provider_payment_id, "status": "captured"}

provider = PaymentProviderStub()

def initiate_payment(db: Session, order_id: int, amount: float, provider_name: str = "stub"):
    resp = provider.create_payment(amount)
    p = Payment(order_id=order_id, amount=amount, provider=provider_name, provider_payment_id=resp["id"], status=resp["status"])
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def capture_payment(db: Session, payment_id: int):
    pay = db.query(Payment).filter(Payment.id == payment_id).first()
    if not pay:
        return None
    resp = provider.capture_payment(pay.provider_payment_id)
    pay.status = resp["status"]
    db.add(pay)
    db.commit()
    db.refresh(pay)
    return pay
