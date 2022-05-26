from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from typing import List
from fastapi_utils.tasks import repeat_every
from fastapi_utils.session import FastAPISessionMaker
import random
import logging
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from sql_app import models
from sql_app.db import get_db, engine
import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.repositories import OfferRepo
from sqlalchemy.orm import Session
from settings import BASE_URL



app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0",)

logging.basicConfig(level=logging.INFO)

models.Base.metadata.create_all(bind=engine)
token = '1sldsfk3jv;x"q3v[5-6gxcw123r'
valid_api_key = '1asaf1KvawkrPdfsd35g'
# BACKGROUND JOB
database_uri = "sqlite:///../data.db"
sessionmaker = FastAPISessionMaker(database_uri)


#TODO add json encoder in set_price
@app.on_event("startup")
@repeat_every(seconds=60)  # 1 minute
def set_price():
    with sessionmaker.context_session() as db:
        random_offer = OfferRepo.select_random_offer(db)
        if random_offer:
            random_offer.price = random.randint(1,100000)
            OfferRepo.update(db=db,offer_data=random_offer)
            logging.info(f'Change offer price with id {random_offer.id}. Price: {random_offer.price} ')
        
        else:
            pass

        



@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

 # OFFERS ------------------------------------------------------------------------------------


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
    else:
        return OfferRepo.fetch_all(db)


@app.get(f'/product/{{offer_id}}{BASE_URL}/', tags=["Offer"], response_model=schemas.Offer)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    """
    Get the Offer with the given ID provided by User stored in database
    """
    # TODO Change Response Model. Delete Product_id from response

    db_offer = OfferRepo.fetch_by_id(db, offer_id)
    if db_offer is None:
        raise HTTPException(
            status_code=404, detail="Offer not found with the given ID")
    return db_offer


@app.post('/products/register', tags=['Offer'], response_model=schemas.Offer)
async def create_offer(offer_request: schemas.OfferCreate, db: Session = Depends(get_db)):
    print(
        f'================================{offer_request}=================================')
    # db_product = OfferRepo.fetch_by_id(db, _id=offer_request.product_id)
    # if db_product:
    #     raise HTTPException(status_code=400, detail="Offer already exists!")

    return await OfferRepo.create(db=db, offer=offer_request)


@app.post('/token', tags=['Offer'], response_model=schemas.Token)
async def get_token(token_request: schemas.APIKey):
    if token_request.api_key == valid_api_key:
        return schemas.Token(token=token)
    return {"message": "Invalid API Key"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
