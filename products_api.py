
from datetime import timedelta
import json
from typing import List, Optional
import requests
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, API_KEY, API_URL
from sql_app import models
from sql_app.db import get_db
from sql_app import schemas
from sql_app.repositories import PriceRepo, ProductRepo, OfferRepo, UserRepo
from fastapi.responses import JSONResponse
# pylint: disable=import-error
# pylint: disable=wrong-import-position

products_api_app = FastAPI()


@products_api_app.exception_handler(Exception)
def validation_exception_handler(request, err):
    "Global exception handler"
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}.Detail: {err}"})


@products_api_app.post('/register', tags=['Auth'])
def register(user_request: schemas.RegisterUser, db: Session = Depends(get_db)):
    """
    Register User and store it in the database
    """
    user_db = UserRepo.fetch_by_name(db=db, username=user_request.username)
    if user_db:
        raise HTTPException(status_code=400, detail="User already exists!")
    hashed_password = get_password_hash(user_request.password) 
    new_user = UserRepo.create(db=db, username=user_request.username, password=hashed_password)
    return {f'Succesfully created user with username {new_user.username}'}


@products_api_app.post("/login", tags=['Auth'], response_model=schemas.AccessToken)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login to get Access Token
    """
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    content = {"access_token": access_token, "token_type": "bearer"}
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    return JSONResponse(content=content, headers=headers)





@products_api_app.post('/products', tags=["Product"], response_model=schemas.Product, status_code=201)
def create_product(product_request: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Create an Product and store it in the database
    """
    db_product = ProductRepo.fetch_by_name(db, name=product_request.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists!")
    new_product = ProductRepo.create(db=db, product=product_request)  
    token = requests.post(f'http://{API_URL}/api/v2/auth',
                      data=json.dumps({'api_key': API_KEY})).json()['token']

    requests.post(f'http://{API_URL}/api/v2/products/register', data=json.dumps(
            {'product_id': new_product.id,
            'token': token
            }
        ))

    return new_product

    

@products_api_app.get('/products', tags=["Product"], response_model=List[schemas.Product])
def get_all_products(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Products stored in database
    """
    if name:
        products = []
        db_product = ProductRepo.fetch_by_name(db, name)
        if db_product is None:
            raise HTTPException(status_code=404, detail='Product not found with the given name')
        products.append(db_product)
        return products
    else:
        return ProductRepo.fetch_all(db)


@products_api_app.get('/products/{product_id}', tags=["Product"], response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get the Product with the given ID provided by User stored in database
    """
    db_product = ProductRepo.fetch_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=404, detail="Product not found with the given ID")
    return db_product


@products_api_app.delete('/products/{product_id}', tags=["Product"])
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Delete the Product with the given ID provided by User stored in database
    """
    db_product = ProductRepo.fetch_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(
            status_code=404, detail="Product not found with the given ID")
    ProductRepo.delete(db, product_id)
    return {'message': f'Product with id {product_id} was successfully deleted'}


@products_api_app.put('/products/{product_id}', tags=["Product"])
def update_product(product_id: int,product_request: schemas.ProductBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Update an Product stored in the database
    """
    db_product = ProductRepo.fetch_by_id(db, product_id)
    if db_product:
        update_item_encoded = jsonable_encoder(product_request)
        db_product.name = update_item_encoded['name']
        db_product.description = update_item_encoded['description']       
        ProductRepo.update(db=db, product_data=db_product)
        return {'message': f'Product with id {product_id} was succesfully updated'}
    else:
        raise HTTPException(
            status_code=400, detail="Product not found with the given ID")

@products_api_app.get('/products/{product_id}/price_history', tags=["Price"], response_model=schemas.PriceHistory )
def get_price_history(product_id: int, db: Session = Depends(get_db)):
    """
    Returns the trend in offer prices
    """
    price_history = PriceRepo.get_price_history(db=db, product_id=product_id)
    if price_history:
        return {"price_history": [price_history]}
    raise HTTPException(
            status_code=404, detail="Product not found with the given ID")

@products_api_app.get('/products/{product_id}/price_change', tags=["Price"])
def get_price_change(from_time: str, to_time: str, product_id: int, db: Session = Depends(get_db)):
    """
    Returns percentual rise/fall for a chosen period of time
    """
    percentual_change = PriceRepo.get_price_change(db=db, from_time=from_time, to_time=to_time, product_id=product_id)
    if percentual_change:
        return {"message": f"Price changed on {percentual_change}%"}