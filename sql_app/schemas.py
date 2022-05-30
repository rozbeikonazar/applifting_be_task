"Create Pydantic schemas"
from typing import Optional
# pylint: disable=no-name-in-module
from pydantic import BaseModel


class OfferBase(BaseModel):
    "Create or read data from Offers API"
    price: int = None
    items_in_stock: int = None
    product_id: int

class OfferCreate(BaseModel):
    "Create data for Offers API"
    product_id: int
    token: Optional[str] = None

class Offer(BaseModel):
    "Read data for Offers API"
    id: int
    price: int = None
    items_in_stock: int = None
    class Config:
        "Configurations to Pydantic"
        orm_mode = True


class ProductBase(BaseModel):
    "Create or read data from Products API"
    name: str
    description: Optional[str] = None


class ProductCreate(ProductBase):
    "Create data for Products API"



class Product(ProductBase):
    "Read data for Products API"

    class Config:
        "Configurations to Pydantic"
        orm_mode = True


class APIKey(BaseModel):
    "Create or Read API key"
    api_key: str

class Token(BaseModel):
    "Create or Read Token"
    token: str
