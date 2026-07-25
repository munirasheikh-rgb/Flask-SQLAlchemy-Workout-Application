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

def test_get_exercise_and_workouts(client):    
    response = client.get("/exercises/1")
    data = response.get_json()
    
    assert response.status_code == 200
    assert  data["id"]==1
    assert "name"in data
    assert "category" in data
    assert "equipment_needed" in data
    assert "workouts" in data

    assert isinstance(data["workouts"],list)

def test_noneexistent_exercise_returns_404(client):
    response = client.get("/exercises/900")
    data = response.get_json()
    assert response.status_code == 404
    assert data["error"] =="Exercise not found"
    
