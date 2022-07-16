'Products API'
import random
import logging
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sql_app import models
from sql_app.db import get_db, engine, SessionLocal
from sql_app.repositories import OfferRepo
# pylint: disable=import-error
# pylint: disable=wrong-import-position
from offers_api import offers_api_app
from products_api import products_api_app
import sqlite3

app = FastAPI()
app.mount("/api/v1",products_api_app)
app.mount("/api/v2",offers_api_app)
logging.basicConfig(level=logging.DEBUG)
models.Base.metadata.create_all(bind=engine)



@app.on_event("startup")
@repeat_every(seconds=60)
def get_last_offer():
    "Background service to get last offers"
    db_session = SessionLocal()
    last_offer = OfferRepo.fetch_all(db_session)[-1]
    logging.info('New/Updated offer is: id=%s, items_in_stock=%s, price=%s',
    last_offer.id, last_offer.items_in_stock, last_offer.price)

@app.on_event("startup")
@repeat_every(seconds=60)  
def set_price():
    "Background service to set price for offers"
    db_session = SessionLocal()
    random_offer = OfferRepo.select_random_offer(db_session)
    if random_offer:
        random_offer.price = random.randint(1,100000)
        OfferRepo.update(db=db_session,offer_data=random_offer)
        logging.info("Change offer price with id %s. Price: %s",
        random_offer.id, random_offer.price)
    else:
        print('No offers yet')

@app.on_event('startup')
def set_trigger():
    con = sqlite3.connect('data/data.db')
    cur = con.cursor()
    cur.execute("""CREATE TRIGGER IF NOT EXISTS price_change
    AFTER UPDATE ON offers
    BEGIN INSERT INTO prices(
    price,
    time,
    product_id
    )
    VALUES(
        new.price,
        DATETIME('NOW'),
        old.product_id
    
    ) ;
    END;
""")
    con.commit()
