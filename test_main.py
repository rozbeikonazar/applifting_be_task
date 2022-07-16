'Tests for products API'

from fastapi.testclient import TestClient
from auth.auth import create_access_token
from main import app
# pylint: disable=wrong-import-position
# pylint: disable=import-error
from settings import API_KEY, BASE_URL
client = TestClient(app)



def test_register():
    #incomplete request
    response = client.post('api/v1/register', json={'username': 'string'})
    assert response.status_code == 422
    #completed request
    response = client.post('api/v1/register', json={'username': 'nazar', 'password': 'nazar'})
    assert response.status_code == 200

TEST_ACCESS_TOKEN = create_access_token(
        data={"sub": "nazar"}, expires_delta=None
    )

def test_login():
    #invalid credentials
    response = client.post('api/v1/login',  data={'username': 'invalid_user', 'password': 'invalid_password'})
    assert response.status_code == 401
    #valid credentials
    response = client.post('api/v1/login',  data={'username': 'nazar', 'password': 'nazar'})
    assert response.status_code == 200


def test_create_product():
    #Unauthorized attempt
    response = client.post('api/v1/products', json={'name':"test", 'description':'test'})
    assert response.status_code == 401
    #Invalid data
    response = client.post('api/v1/products', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'description':'test'})
    assert response.status_code == 422
    #Authorized and valid data
    response = client.post('api/v1/products',headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"string", 'description':'string'})
    assert response.status_code == 201
    #Product already exist
    response = client.post('api/v1/products', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"string", 'description':'string'})
    assert response.status_code == 400



def test_get_product():
    "TEST: Get the Product with the given ID"
    #Not existing product_id
    response = client.get(f"api/v1/products/666")
    assert response.status_code == 404
    #Valid product_id
    product_id = 1
    response = client.get(f"api/v1/products/{product_id}")
    assert response.status_code == 200
    name = response.json().get('name')
    description = response.json().get('description')
    assert name == 'string'
    assert description == 'string'

    

def test_get_all_products():
    "Get all the Products stored in database"
    #Invalid name
    response = client.get('api/v1/products?name=sdasdasdasdas')
    assert response.status_code == 404
    #Valid name
    response = client.get('api/v1/products')
    assert response.status_code == 200
    assert len(response.json()) == 1
    name = response.json()[0]['name']
    description = response.json()[0]['description']
    assert name == 'string'
    assert description == 'string'


def test_update_product():
    product_id = 1    
    #Unauthorized attempt
    response = client.put(f'api/v1/products/{product_id}', json={'name':"test", 'description':'test'})
    assert response.status_code == 401
    #Not existing product_id
    response = client.put(f'api/v1/products/666', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test", 'description':'test'})
    assert response.status_code == 400
    #Invalid data
    response = client.put(f'api/v1/products/{product_id}', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'description':'test'})
    assert response.status_code == 422
    #Authorized and valid data
    response = client.put(f'api/v1/products/{product_id}', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test", 'description':'test'})
    assert response.status_code == 200

def test_get_offer():
    "Get the Offer with the given ID"
    offer_id = 1
    #Not existing offer_id
    response = client.get(f"api/v2/product/666{BASE_URL}/")
    assert response.status_code == 404
    response = client.get(f"api/v2/product/{offer_id}{BASE_URL}/")
    assert response.status_code == 200

def test_register_product():
    #Invalid data
    response = client.post(f'api/v2/products/register', json={'product_id': 'Not int'})
    assert response.status_code == 422
    #Valid data
    response = client.post(f'api/v2/products/register', json={'product_id': 1})
    assert response.status_code == 200

def test_auth():
    #Incorrect api_key
    response = client.post(f'api/v2/auth', json={'api_key':'fakeapikey'})
    assert response.status_code == 404
    response = client.post(f'api/v2/auth', json={'api_key': API_KEY})
    assert response.status_code == 200

def test_delete_product():
    "Delete the Product with the given ID"
    product_id = 1
    #Unauthorized attempt
    response = client.delete(f'api/v1/products/{product_id}', json={'name':"test1", 'description':'test1'})
    assert response.status_code == 401
    #Not existing product_id
    response = client.delete(f'api/v1/products/666', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test1", 'description':'test1'})
    assert response.status_code == 404
    #Authorized and valid data
    response = client.delete(f'api/v1/products/{product_id}', headers={'Authorization': 'Bearer {}'.format(TEST_ACCESS_TOKEN)}, json={'name':"test1", 'description':'test1'})
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Product with id {product_id} was successfully deleted"
    }




