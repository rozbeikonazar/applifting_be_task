from fastapi.testclient import TestClient

from main import app
from settings import BASE_URL
client = TestClient(app)


#TODO mock db
def test_get_offer():
    offer_id = 1
    response = client.get(f"/product/{offer_id}{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {
    "id": 1,
    "price": 'null',
    "items_in_stock": 'null'
    }

def test_get_all_offers():
    response = client.get(f'{BASE_URL}')
    assert response.status_code == 200
    assert response.json == {
        
    }