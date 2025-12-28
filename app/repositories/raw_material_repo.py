from app.models.raw_material import RawMaterial
from .base import BaseRepository




class RawMaterialRepository(BaseRepository["RawMaterial"]):
    MODEL = RawMaterial
