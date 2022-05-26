from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .db import Base


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float(precision=2), nullable=True)
    items_in_stock = Column(Integer, nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False) 

    def __repr__(self):
        return f'OffersModel(price={self.price}, items_in_stock={self.items_in_stock}, id={self.id})'


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True, index=True)
    description = Column(String(255))
   

    def __repr__(self):
        return f'ProductModel(name={self.name}, '