from fastapi import FastAPI
from app.endpoints.order_endpoints import order_endpoint
from app.endpoints.items_endpoints import order_items_endpoints
from app.endpoints.auth_endpoints import auth_endpoints
from app.endpoints.order_item_endpoints import order_item_endpoints
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.company_endpoints import company_endpoints
from app.endpoints.drive_endponts import drive_endpoints

version = "v1"

app = FastAPI(
    version = version
        )

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware , 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




app.include_router(order_endpoint , prefix=f"/api/{version}/orders")
app.include_router(order_items_endpoints , prefix=f"/api/{version}/orders/{{order_id}}/items")
app.include_router(auth_endpoints , prefix=f"/api/{version}/auth")
app.include_router(order_item_endpoints , prefix=f"/api/{version}/items")
app.include_router(company_endpoints , prefix=f"/api/{version}/company")
app.include_router(drive_endpoints , prefix=f"/api/{version}/drive")

@app.get("/")
def home():
    return "home routes"
