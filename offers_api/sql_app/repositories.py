from sqlalchemy.orm import Session

from . import models, schemas


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
        
    async def update(db: Session, offer_data):
        updated_product = db.merge(offer_data)
        db.commit()
        return updated_product