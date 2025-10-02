from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.item_model import Item
from backend.schemas.item_schema import ItemSchema

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/")
def create_item(item: ItemSchema, db: Session = Depends(get_db)):
    try:
        db_item = Item(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return {"status": "success", "data": db_item}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_items(db: Session = Depends(get_db)):
    return {"status": "success", "data": db.query(Item).all()}
