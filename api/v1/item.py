from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.v1 import get_db
from api.v1 import item_type as itype
from db import crud, schema


router = APIRouter()


@router.post("/", response_model=schema.Item)
def create_item(item: schema.ItemCreate, db: Session = Depends(get_db)):
    itype.is_item_type_exists(db, item.type_id)
    return crud.create_item(db, item)


@router.get("/", response_model=List[schema.Item])
def read_items(limit: int = 100, offset: int = 0, item_type: int = 0, db: Session = Depends(get_db)):
    itype.is_item_type_exists(db, item_type)
    items = crud.get_items(db, limit=limit, offset=offset, item_type=item_type)
    return items


@router.get("/{item_id}", response_model=schema.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, row_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", response_model=schema.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, row_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item)
    return item


@router.patch('/{item_id}/balance', response_model=schema.Item)
def patch_balance(item_id: int, item_balance: schema.ItemBalancePatch, db: Session = Depends(get_db)):
    item = crud.get_item(db, row_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item_balance(db, item, item_balance.balance)
