from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import auth, categories, products, cart, orders, payments,admin

# ensure tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ecommerce Platform - Phase 2")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(admin.router)
