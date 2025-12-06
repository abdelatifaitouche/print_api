from fastapi import APIRouter



order_items_endpoints = APIRouter()






@order_items_endpoints.get("/")
def home():
    return "items home"
