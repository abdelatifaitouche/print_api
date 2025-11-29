from fastapi import FastAPI
from app.endpoints.order_endpoints import order_endpoint



app = FastAPI()

app.include_router(order_endpoint , prefix="/orders")


@app.get("/")
def home():
    return "home routes"
