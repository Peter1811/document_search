from pydantic import BaseModel

class DocumentCreate(BaseModel):
    text: str