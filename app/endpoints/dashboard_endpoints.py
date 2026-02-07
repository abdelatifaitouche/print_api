from fastapi import APIRouter


dashboard = APIRouter()


@dashboard.get("/")
def list():
    return
