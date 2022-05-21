from typing import List, Optional

from pydantic import BaseModel



class OfferBase(BaseModel):
    
    price: int = None
    items_in_stock: int = None
    product_id: int

class OfferCreate(BaseModel):
    product_id: int


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




