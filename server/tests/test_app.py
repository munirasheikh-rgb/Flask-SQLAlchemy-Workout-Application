import pytest 
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] =True
    with app.test_client()as client:
        yield client

def test_get_all_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200
    assert isinstance(response.get_json(),list)