from typing import List, Optional

from pydantic import BaseModel


class OfferBase(BaseModel):
    
    price: int
    items_in_stock: int
    product_id: int

class OfferCreate(OfferBase):
    price: Optional[int] = 0
    items_in_stock: Optional[int] = 0
    product_id: Optional[int] = 0


class Offer(OfferBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True




class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    


class ProductCreate(ProductBase):
    id: int


class Product(ProductBase):
    id: int
    offers: List[Offer] = []
    
    class Config:
        orm_mode = True







