from fastapi import FastAPI
from app.endpoints.order_endpoints import order_endpoint
from app.endpoints.items_endpoints import order_items_endpoints
from app.endpoints.auth_endpoints import auth_endpoints

version = "v1"

app = FastAPI(
    version = version
        )

app.include_router(order_endpoint , prefix=f"/api/{version}/orders")
app.include_router(order_items_endpoints , prefix=f"/api/{version}/orders/{{order_id}}/items")
app.include_router(auth_endpoints , prefix=f"/api/{version}/auth")




@app.get("/")
def home():
    return "home routes"
