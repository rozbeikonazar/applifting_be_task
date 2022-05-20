from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sql_app import models
from sql_app.db import get_db, engine
import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.repositories import ProductRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
import requests, json


app = FastAPI(title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",)


models.Base.metadata.create_all(bind=engine)








@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})





#PRODUCTS

@app.post('/products', tags=["Product"], response_model=schemas.Product, status_code=201)
async def create_product(product_request: schemas.ProductCreate, offer_request: schemas.OfferCreate,  db: Session = Depends(get_db)):
    """
    Create an Product and store it in the database
    """
    
    db_product = ProductRepo.fetch_by_id(db, _id=product_request.id)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists!")
     
    # some_info = {'info':'some_info'}
    # head = 'http://192.168.0.8:8000/' #IP and port of your server 
    # # maybe in your case the ip is the localhost 
    # requests.post(f'{head}/send_some_info', data=json.dumps(some_info))
    
    
    return await ProductRepo.create(db=db, product=product_request)

   

@app.get('/products', tags=["Product"],response_model=List[schemas.Product])
def get_all_products(name: Optional[str] = None,db: Session = Depends(get_db)):
    """
    Get all the Products stored in database
    """
    if name:
        products =[]
        db_product = ProductRepo.fetch_by_name(db,name)
        products.append(db_product)
        return products
    else:
        return ProductRepo.fetch_all(db)


@app.get('/products/{product_id}', tags=["Product"],response_model=schemas.Product)
def get_product(product_id: int,db: Session = Depends(get_db)):
    """
    Get the Product with the given ID provided by User stored in database
    """
    db_product = ProductRepo.fetch_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found with the given ID")
    return db_product

@app.delete('/products/{product_id}', tags=["Product"])
async def delete_product(product_id: int,db: Session = Depends(get_db)):
    """
    Delete the Product with the given ID provided by User stored in database
    """
    db_product = ProductRepo.fetch_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found with the given ID")
    await ProductRepo.delete(db,product_id)
    return "Product deleted successfully!"

@app.put('/products/{product_id}', tags=["Product"],response_model=schemas.Product)
async def update_product(product_id: int, product_request: schemas.Product, db: Session = Depends(get_db)):
    """
    Update an Product stored in the database
    """
    db_product = ProductRepo.fetch_by_id(db, product_id)
    if db_product:
        update_item_encoded = jsonable_encoder(product_request)
        db_product.name = update_item_encoded['name']
        db_product.description = update_item_encoded['description']
        db_product.offers = update_item_encoded['offers']
        return await ProductRepo.update(db=db, product_data=db_product)
    else:
        raise HTTPException(status_code=400, detail="Product not found with the given ID")






if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)