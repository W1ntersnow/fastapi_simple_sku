from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.v1 import get_db
from db import crud, schema


router = APIRouter()


def is_item_type_exists(db, item_type_id):
    if not item_type_id:
        return
    item_type = crud.get_item_type(db, item_type_id)
    if item_type is None:
        raise HTTPException(status_code=404, detail="ItemType not found")


@router.post("/", response_model=schema.ItemType)
def create_item_type(row: schema.ItemTypeCreate, db: Session = Depends(get_db)):
    return crud.create_item_type(db, row)


@router.get("/", response_model=List[schema.ItemType])
def get_item_types(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return crud.get_item_types(db, limit, offset)
