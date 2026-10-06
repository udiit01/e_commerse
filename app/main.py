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


print("CART MODULE:", cart.__file__)

print("CART ROUTER ROUTES:")
for route in cart.router.routes:
    print(route.path, route.methods)

print("APP ROUTES:")
for route in app.routes:
    print(route.path, route.methods)