# from typing import List
from pydantic import BaseModel


class ItemBalancePatch(BaseModel):
    balance: int


class ItemBase(BaseModel):
    title: str
    description: str
    sku: str
    type_id: int
    balance: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class ItemTypeBase(BaseModel):
    title: str
    description: str


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemType(ItemTypeBase):
    id: int

    class Config:
        orm_mode = True



