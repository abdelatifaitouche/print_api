from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.endpoints.order_endpoints import order_endpoint
from app.endpoints.items_endpoints import order_items_endpoints
from app.endpoints.auth_endpoints import auth_endpoints
from app.endpoints.items_endpoints import order_items_endpoints
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.company_endpoints import company_endpoints
from app.endpoints.drive_endponts import drive_endpoints
from app.endpoints.raw_material_endpoints import raw_material_endpoints
from app.endpoints.product_endpoints import product_endpoints
from app.execeptions.exceptions_handlers import register_exception_handlers


version = "v1"

app = FastAPI(version=version, redirect_slashes=False)
register_exception_handlers(app)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(order_endpoint, prefix=f"/api/{version}/orders")
app.include_router(auth_endpoints, prefix=f"/api/{version}/auth")
app.include_router(order_items_endpoints, prefix=f"/api/{version}/items")
app.include_router(company_endpoints, prefix=f"/api/{version}/company")
app.include_router(drive_endpoints, prefix=f"/api/{version}/drive")
app.include_router(raw_material_endpoints, prefix=f"/api/{version}/materials")
app.include_router(product_endpoints, prefix=f"/api/{version}/products")
