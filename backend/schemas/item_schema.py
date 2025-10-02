from pydantic import BaseModel
from typing import Optional

class ItemSchema(BaseModel):
    id: Optional[int]
    invoice_id: int
    name: str
    price: float

    class Config:
        orm_mode = True
