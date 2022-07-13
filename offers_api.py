"Offers API"
import json
import logging
import random
from fastapi_utils.tasks import repeat_every
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
# pylint: disable=wrong-import-position
# pylint: disable=import-error
from sql_app.db import get_db, SessionLocal
from sql_app import schemas
from sql_app.repositories import OfferRepo
from settings import TOKEN, API_KEY

logging.basicConfig(level=logging.DEBUG)



class OffersAPI:
    
    def validation_exception_handler(request, err):
        "Global exception handler"
        base_error_message = f"Failed to execute: {request.method}: {request.url}"
        return JSONResponse(status_code=400, content={"message": f"{base_error_message}.Detail: {err}"})
    
    
    def get_token(token_request: schemas.APIKey):
        "Check API key and return token"
        if json.loads(token_request)["api_key"] == API_KEY:
            return schemas.Token(token=TOKEN)
        raise HTTPException(
            status_code=404, detail="API key is incorrect")
    
    def create_offer(offer_request: schemas.OfferCreate, db: Session = Depends(get_db)):
        "Register product"
        return OfferRepo.create(db=db, offer=offer_request)