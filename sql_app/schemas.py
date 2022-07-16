"Create Pydantic schemas"
from typing import List, Optional, Union
# pylint: disable=no-name-in-module
from pydantic import BaseModel


class OfferBase(BaseModel):
    "Create or read data from Offers API"
    price: int = None
    items_in_stock: int = None
    id: int

class OfferCreate(BaseModel):
    "Create data for Offers API"
    product_id: int

class Offer(OfferBase):
    "Read data for Offers API"
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
    offers: List[Offer] = []
    class Config:
        "Configurations to Pydantic"
        orm_mode = True


class APIKey(BaseModel):
    "Create or Read API key"
    api_key: str

class Token(BaseModel):
    "Create or Read Token"
    token: str

class User(BaseModel):
    username: str
    password: str
    class Config:
        orm_mode = True

class RegisterUser(BaseModel):
    username: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
