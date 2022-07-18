"Offers API"
import logging
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
# pylint: disable=wrong-import-position
# pylint: disable=import-error
from sql_app.db import get_db
from sql_app import schemas
from sql_app.repositories import OfferRepo
from settings import BASE_URL, TOKEN, API_KEY
logging.basicConfig(level=logging.DEBUG)

offers_api_app = FastAPI()


@offers_api_app.exception_handler(Exception)
def validation_exception_handler(request, err):
    "Global exception handler"
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}.Detail: {err}"})


@offers_api_app.post('/products/register', tags=['Auth'], response_model=schemas.Offer)
def register_product(offer_request: schemas.OfferCreate, db: Session = Depends(get_db)):
    "Register product"
    return OfferRepo.create(db=db, offer=offer_request)
    

@offers_api_app.post('/auth', tags=['Auth'], response_model=schemas.Token)
def send_token(token_request: schemas.APIKey):
    "Check API key and return token"
    if token_request.api_key == API_KEY:
        return schemas.Token(token=TOKEN)
    raise HTTPException(status_code=404, detail='API key is incorrect')


@offers_api_app.get(f'/product/{{offer_id}}{BASE_URL}/', tags=["Offer"], response_model=schemas.Offer)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    """
    Get the Offer with the given ID provided by User stored in database
    """

    db_offer = OfferRepo.fetch_by_id(db, offer_id)
    if db_offer is None:
        raise HTTPException(
            status_code=404, detail="Offer not found with the given ID")
    return db_offer