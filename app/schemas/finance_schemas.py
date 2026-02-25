from pydantic import BaseModel


class BaseDocument(BaseModel):
    id: str
    document_type: str
