from fastapi import FastAPI
from app.endpoints.order_endpoints import order_endpoint

version = "v1"

app = FastAPI(
    version = version
        )

app.include_router(order_endpoint , prefix=f"/api/{version}/orders")


@app.get("/")
def home():
    return "home routes"
