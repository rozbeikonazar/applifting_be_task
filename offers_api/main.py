from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sql_app import models
from sql_app.db import get_db, engine
import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.repositories import OfferRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",)

models.Base.metadata.create_all(bind=engine)








@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})






 #OFFERS ------------------------------------------------------------------------------------   





@app.get('/offers', tags=["Offer"],response_model=List[schemas.Offer])
def get_all_offers(_id: int = None,db: Session = Depends(get_db)):
    """
    Get all the Offers stored in database
    """
    if _id:
        offers =[]
        db_offer = OfferRepo.fetch_by_id(db, _id)
        
        offers.append(db_offer)
        return offers
    else:
        return OfferRepo.fetch_all(db)
    
@app.get('/offers/{offer_id}', tags=["Offer"],response_model=schemas.Offer)
def get_offer(offer_id: int,db: Session = Depends(get_db)):
    """
    Get the Offer with the given ID provided by User stored in database
    """
    db_offer = OfferRepo.fetch_by_id(db,offer_id)
    if db_offer is None:
        raise HTTPException(status_code=404, detail="Offer not found with the given ID")
    return db_offer

# @app.delete('/offers/{offer_id}', tags=["Offer"])
# async def delete_offer(offer_id: int,db: Session = Depends(get_db)):
#     """
#     Delete the Offer with the given ID provided by User stored in database
#     """
#     db_offer = OfferRepo.fetch_by_id(db,offer_id)
#     if db_offer is None:
#         raise HTTPException(status_code=404, detail="Offer not found with the given ID")
#     await OfferRepo.delete(db,offer_id)
#     return "Offer deleted successfully!"
#TODO ADD NAME and DESCRIPTION
@app.post('/products/register', tags=['Offer'], response_model=schemas.CreateOffer)
def passss():
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)