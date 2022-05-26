from re import L
from sqlalchemy.orm import Session

from . import models, schemas
import random

class OfferRepo:
    
    async def create(db: Session, offer: schemas.OfferCreate):
            #db_offer = models.Offer(price=offer.price, items_in_stock=offer.items_in_stock, product_id=offer.product_id)
            db_offer = models.Offer(product_id=offer.product_id)
            db.add(db_offer)
            db.commit()
            db.refresh(db_offer)
            return db_offer
        
    def fetch_by_id(db: Session, _id:int):
        return db.query(models.Offer).filter(models.Offer.id == _id).first()

    
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Offer).offset(skip).limit(limit).all()
    
    async def delete(db: Session,_id:int):
        db_product = db.query(models.Offer).filter_by(id=_id).first()
        db.delete(db_product)
        db.commit()
        
    #WAS an a async func
    def update(db: Session, offer_data):
        updated_product = db.merge(offer_data)
        db.commit()
        return updated_product

    def select_random_offer(db: Session):
        offers = OfferRepo.fetch_all(db=db)
        random_offer = random.choice(offers)
        return random_offer

#PRODUCT rep
class ProductRepo:
    
 async def create(db: Session, product: schemas.ProductCreate):
        db_product = models.Product(name=product.name,description=product.description,)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
 def fetch_by_id(db: Session, _id):
     return db.query(models.Product).filter(models.Product.id == _id).first()
 
 def fetch_by_name(db: Session,name):
     return db.query(models.Product).filter(models.Product.name == name).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Product).offset(skip).limit(limit).all()
 
 async def delete(db: Session,product_id):
     db_product = db.query(models.Product).filter_by(id=product_id).first()
     db.delete(db_product)
     db.commit()
     
     
 async def update(db: Session,product_data):
    updated_product = db.merge(product_data)
    db.commit()
    return updated_product
    