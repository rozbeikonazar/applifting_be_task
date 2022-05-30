'Tests for products API'

import sys
import os
from fastapi.testclient import TestClient
from main import app
# pylint: disable=wrong-import-position
# pylint: disable=import-error
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from sql_app.db import SessionLocal
from sql_app.repositories import ProductRepo
from sql_app import schemas
client = TestClient(app)



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
    print(type(response))
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



def test_update_product():
    "Update an Product stored in the database"
    product_id = 2
    response = client.put(f'/products/{product_id}',
    json={"name":"string1448", "description": "string"})
    assert response.status_code == 200
    assert response.json() == {
      "name":"string1448",
      "description": "string"
    }

def test_delete_product():
    "Delete the Product with the given ID"
    product_id = 2
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.json() == {
        "message": "Product with id 2 was successfully deleted"
    }
