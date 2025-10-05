# backend/schemas/item_schema.py
from pydantic import BaseModel
from typing import Optional

class ItemSchema(BaseModel):
    id: Optional[int]
    invoice_id: int
    description: str
    quantity: int = 1
    unit_price: float = 0.0
    total: float = 0.0

    class Config:
        orm_mode = True
