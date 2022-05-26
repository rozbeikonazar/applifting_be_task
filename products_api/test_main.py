from fastapi.testclient import TestClient

from main import app, token

client = TestClient(app)



#TODO mock db
def test_get_product():
    product_id = 1
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {
        'name': 'string',
        'description': 'string'
    }


def test_get_all_products():
    response = client.get(f'/products')
    assert response.status_code == 200
    assert response.json() == [
  {
    "name": "string",
    "description": "string"
  },
  {
    "name": "string2",
    "description": "string2"
  }
]

#TODO update_product
# def test_update_product():
#     product_id = 1
#     response = client.put(f'/products/{product_id}')
#     assert response.status_code == 200
#     assert response.json() == {

#     }

def test_delete_product():
    product_id = 2
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.json == {
        'message': 'Product with id 2 was successfully deleted'
    }


#TODO FIX test_create_product
# def test_create_product():
#     response = client.post(
#         '/products/',
#         json={'name': 'Pytest', 'description' : 'Pytest'})
#     print(f'RESPONSE============={response.url}')
#     assert response.status_code == 200
#     assert response.json() == {
#         'name': 'Pytest',
#         'description' : 'Pytest',
#         'token': token
#     }