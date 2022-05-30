'Tests for offers API'
import os
import sys
# pylint: disable=wrong-import-position
# pylint: disable=import-error
from fastapi.testclient import TestClient
from main import app
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from settings import BASE_URL
client = TestClient(app)



def test_get_offer():
    "Get the Offer with the given ID"
    offer_id = 1
    response = client.get(f"/product/{offer_id}{BASE_URL}/")
    assert response.status_code == 200

def test_get_all_offers():
    "Get all Offers stored in database"
    response = client.get(f'{BASE_URL}')
    assert response.status_code == 200
