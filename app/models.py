from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class UserItem(Base):
    __tablename__ = "user_item"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id", ondelete='CASCADE'), nullable=False)

    items = relationship("Item", back_populates="user_item", cascade='all,delete')
    users = relationship("User", back_populates="user_item", cascade='all,delete')


user_item = UserItem.__table__


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    items = relationship("Item", secondary=UserItem, back_populates="users")


users = User.__table__


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    users = relationship("User", secondary=UserItem, back_populates="items")


items = Item.__table__
