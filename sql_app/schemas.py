from typing import List, Optional

from pydantic import BaseModel


class OfferBase(BaseModel):

    price: int = None
    items_in_stock: int = None
    product_id: int
    

class OfferCreate(BaseModel):
    product_id: int
    token: Optional[str] = None

class Offer(BaseModel):
    id: int
    price: int = None
    items_in_stock: int = None
    
    
    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    #id: int
    #offers: List[Offer] = []

    class Config:
        orm_mode = True


class APIKey(BaseModel):
    api_key: str


class Token(BaseModel):
    token: str
