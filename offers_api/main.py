"Offers API"
import sys
import os
import logging
from typing import List
import random
from fastapi_utils.tasks import repeat_every
#from fastapi_utils.session import FastAPISessionMaker
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn
# pylint: disable=wrong-import-position
# pylint: disable=import-error
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from sql_app import models
from sql_app.db import get_db, engine, SessionLocal
from sql_app import schemas
from sql_app.repositories import OfferRepo
from settings import BASE_URL, TOKEN, API_KEY







app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0",)
logging.basicConfig(level=logging.DEBUG)

models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
@repeat_every(seconds=60)  
def set_price():
    "Background service to set price fo offers"
    db_session = SessionLocal()
    random_offer = OfferRepo.select_random_offer(db_session)
    if random_offer:
        random_offer.price = random.randint(1,100000)
        OfferRepo.update(db=db_session,offer_data=random_offer)
        logging.info("Change offer price with id %s. Price: %s",
        random_offer.id, random_offer.price)
    else:
        print('no offers yet')




@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    "Global exception handler"
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}.Detail: {err}"})

@app.get(f'{BASE_URL}', tags=["Offer"], response_model=List[schemas.Offer])
def get_all_offers(_id: int = None, db: Session = Depends(get_db)):
    """
    Get all the Offers stored in database
    """
    if _id:
        offers = []
        db_offer = OfferRepo.fetch_by_id(db, _id)

        offers.append(db_offer)
        return offers
    return OfferRepo.fetch_all(db)


@app.get(f'/product/{{offer_id}}{BASE_URL}/', tags=["Offer"], response_model=schemas.Offer)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    """
    Get the Offer with the given ID provided by User stored in database
    """

    db_offer = OfferRepo.fetch_by_id(db, offer_id)
    if db_offer is None:
        raise HTTPException(
            status_code=404, detail="Offer not found with the given ID")
    return db_offer


@app.post('/products/register', tags=['Offer'], response_model=schemas.Offer)
def create_offer(offer_request: schemas.OfferCreate, db: Session = Depends(get_db)):
    "Register product"
    return OfferRepo.create(db=db, offer=offer_request)


@app.post('/token', tags=['Offer'], response_model=schemas.Token)
def get_token(token_request: schemas.APIKey):
    "Check API key and return token"
    if token_request.api_key == API_KEY:
        return schemas.Token(token=TOKEN)
    return {"message": "Invalid API Key"}


