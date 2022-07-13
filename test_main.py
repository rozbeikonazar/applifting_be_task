'Tests for products API'

from fastapi.testclient import TestClient
from auth.auth import create_access_token
from main import app
# pylint: disable=wrong-import-position
# pylint: disable=import-error
from sql_app.db import SessionLocal
from sql_app.repositories import ProductRepo
from sql_app import schemas
from settings import BASE_URL
client = TestClient(app)


#Надо ли проверять на слишком длинную строку


TEST_USER = {"username": "nazar", "password": "nazar"}
TEST_ACCESS_TOKEN = create_access_token(
        data={"sub": TEST_USER["username"]}, expires_delta=None
    )
def test_register():
    #incomplete request
    response = client.post('/register', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'username': 'string'})
    assert response.status_code == 422
    #completed request
    response = client.post('/register', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'username': 'test_user2', 'password': 'password'})
    assert response.status_code == 200

def test_login():
    #invalid credentials
    response = client.post('/login',  data={'username': 'invalid_user', 'password': 'invalid_password'})
    assert response.status_code == 401
    #valid credentials
    response = client.post('/login',  data={'username': 'test_user', 'password': 'password'})
    assert response.status_code == 200

def test_get_product():
    "TEST: Get the Product with the given ID"
    #Not existing product_id
    response = client.get(f"/products/666")
    assert response.status_code == 404
    #Valid product_id
    product_id = 18
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    name = response.json().get('name')
    description = response.json().get('description')
    assert name == 'string'
    assert description == 'string'

    

def test_get_all_products():
    "Get all the Products stored in database"
    #Попробовать передать невалидный name в get request!!!
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json()) == 1
    name = response.json()[0]['name']
    description = response.json()[0]['description']
    assert name == 'string'
    assert description == 'string'


def test_create_product():
    #Unauthorized attempt
    response = client.post('/products', json={'name':"test", 'description':'test'})
    assert response.status_code == 401
    #Invalid data
    response = client.post('/products',headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'description':'test'})
    assert response.status_code == 422
    #Product already exist
    response = client.post('/products', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"string", 'description':'string'})
    assert response.status_code == 400
    #Authorized and valid data
    response = client.post('/products',headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test", 'description':'test'})
    assert response.status_code == 201

def test_update_product():
    product_id = 35    
    #Unauthorized attempt
    response = client.put(f'/products/{product_id}', json={'name':"test", 'description':'test'})
    assert response.status_code == 401
    #Not existing product_id
    response = client.put(f'/products/666', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test", 'description':'test'})
    assert response.status_code == 400
    #Invalid data
    response = client.put(f'/products/{product_id}', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'description':'test'})
    assert response.status_code == 422
    #Authorized and valid data
    response = client.put(f'/products/{product_id}', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test", 'description':'test'})
    assert response.status_code == 200


def test_delete_product():
    "Delete the Product with the given ID"
    product_id = 35
    #Unauthorized attempt
    response = client.delete(f'/products/{product_id}', json={'name':"test1", 'description':'test1'})
    assert response.status_code == 401
    #Not existing product_id
    response = client.delete(f'/products/666', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test1", 'description':'test1'})
    assert response.status_code == 404
    #Authorized and valid data
    response = client.delete(f'/products/{product_id}', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test1", 'description':'test1'})
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Product with id {product_id} was successfully deleted"
    }


def test_get_offer():
    "Get the Offer with the given ID"
    offer_id = 9
    #Not existing offer_id
    response = client.get(f"/product/666{BASE_URL}/")
    assert response.status_code == 404
    response = client.get(f"/product/{offer_id}{BASE_URL}/")
    assert response.status_code == 200

def test_get_all_offers():
    #Тоже самое что и с get_all_products
    "Get all Offers stored in database"
    response = client.get(f'{BASE_URL}')
    assert response.status_code == 200