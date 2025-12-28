from app.models.product import ProductModel
from .base import BaseRepository


class ProductRepository(BaseRepository["ProductModel"]):
    MODEL = ProductModel
