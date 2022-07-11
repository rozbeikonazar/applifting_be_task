'Tests for products API'

from fastapi.testclient import TestClient
from main import app
# pylint: disable=wrong-import-position
# pylint: disable=import-error
from sql_app.db import SessionLocal
from sql_app.repositories import ProductRepo
from sql_app import schemas
from settings import BASE_URL
client = TestClient(app)



#TODO fix test_delete_product, test_update_product and add test_login

def test_get_product():
    "TEST: Get the Product with the given ID"
    product_id = 1
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {
        'name': 'string',
        'description': 'string'
    }

def test_get_all_products():
    "Get all the Products stored in database"
    response = client.get('/products')
    assert response.status_code == 200
    assert response.json() == [
  {
    "name": "string",
    "description": "string"
  },

]



def test_create_product():
    "Create an Product and store it in the database"
    db_session = SessionLocal()
    product = schemas.ProductCreate(name='string2', description='string2')
    new_product = ProductRepo.create(db=db_session, product=product)

    assert new_product.name == "string2"
    assert new_product.description == "string2"



# def test_update_product():
#     "Update an Product stored in the database"
#     db_session = SessionLocal()
#     product = schemas.ProductBase(name='string228', description='string228')
#     #response = client.put(f'/products/{2}',
#     #json={"name":"string1448", "description": "string"})
#     updated_product = ProductRepo.update(db=db_session, product_data=product)
#     # assert response.status_code == 200
#     # assert response.json() == {
#     #   "name":"string1448",
#     #   "description": "string"
#     # }
#     assert updated_product.name == 'string228'
#     assert updated_product.description == 'string228'

def test_delete_product():
    "Delete the Product with the given ID"
    product_id = 2
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.json() == [{
        "message": "Product with id 2 was successfully deleted"
    }]


def test_get_offer():
    "Get the Offer with the given ID"
    offer_id = 1
    response = client.get(f"/product/{offer_id}{BASE_URL}/")
    assert response.status_code == 200

def test_get_all_offers():
    "Get all Offers stored in database"
    response = client.get(f'{BASE_URL}')
    assert response.status_code == 200