from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class ItemType(Base):
    __tablename__ = "item_types"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)

    items = relationship("Item", back_populates="type")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    sku = Column(String)
    balance = Column(Integer, default=0)
    description = Column(String)

    type_id = Column(Integer, ForeignKey("item_types.id"))

    type = relationship("ItemType", back_populates="items")
