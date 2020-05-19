from sqlalchemy.orm import Session

from . import models, schema


def _create_row(db, db_item):
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_item(db: Session, row: schema.ItemCreate):
    return _create_row(db, models.Item(**row.dict()))


def create_item_type(db: Session, row: schema.ItemTypeCreate):
    return _create_row(db, models.ItemType(**row.dict()))


def get_item(db: Session, row_id: int):
    return db.query(models.Item).filter(models.Item.id == row_id).first()


def get_item_type(db: Session, row_id: int):
    return db.query(models.ItemType).filter(models.ItemType.id == row_id).first()


def get_item_types(db: Session, limit: int = 100, offset: int = 0):
    return db.query(models.ItemType).offset(offset).limit(limit).all()


def get_items(db: Session, limit: int = 100, offset: int = 0, item_type: int = 0):
    if item_type:
        return db.query(models.Item).filter_by(type_id=item_type).offset(offset).limit(limit).all()
    return db.query(models.Item).offset(offset).limit(limit).all()


def delete_item(db: Session, row: int):
    db.query(models.Item).filter(models.Item.id == row.id).delete()
    db.commit()
    return row


def update_item_balance(db: Session, row: int, balance: int):
    db.query(models.Item).filter(models.Item.id == row.id).update({models.Item.balance: balance})
    db.commit()
    db.refresh(row)
    return row

