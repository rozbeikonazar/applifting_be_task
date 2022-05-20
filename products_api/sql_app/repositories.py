from sqlalchemy.orm import Session

from . import models, schemas


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
    
    

        
