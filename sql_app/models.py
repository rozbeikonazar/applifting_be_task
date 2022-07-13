"Creating a database models"
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from .db import Base
from sqlalchemy.orm import relationship



class Offer(Base):
    "Creating model for Offer API"
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float(precision=2), nullable=True)
    items_in_stock = Column(Integer, nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    def __repr__(self):
        return f'OfferModel(price={self.price}, items_in_stock={self.items_in_stock}, id={self.id})'

class Product(Base):
    "Creating model for Product API"
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True, index=True)
    description = Column(String(255))
    offers =  relationship('Offer',
                            cascade='all, delete-orphan')
    def __repr__(self):
        return f'ProductModel(name={self.name}, '

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String(32), nullable=False, unique=True, index=True)
    password = Column(String(64), nullable=False)
    def __repr__(self):
        return f'UsersModel(username={self.username})'