import pytest 
from app import app
from models import db,Exercise,Workout,WorkoutExercise

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
    response = client.get("/exercises/2")
    data = response.get_json()

    assert response.status_code == 200
    assert  data["id"]==2
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
    
def test_create_exercise(client):
    response = client.post("/exercises",json={
        "name":"jump rope",
        "category":"cardio",
        "equipment_needed":True
    })

    data =response.get_json()
    exercise = db.session.get(Exercise,data["id"])
    assert response.status_code == 201
    assert data["id"] is not None
    assert  data["name"] == "jump rope"
    assert  data["category"] == "cardio"
    assert  data ["equipment_needed"] is True

    db.session.delete(exercise)
    db.session.commit()

def test_create_exercise_saves_to_database(client):
    response = client.post("/exercises",json={
        "name":"jump rope",
        "category":"cardio",
        "equipment_needed":True
    })
    data = response.get_json()

    exercise =db.session.get(Exercise,data["id"])
    assert response.status_code == 201
    assert exercise is not None
    assert exercise.name =="jump rope"
    assert exercise.category == "cardio"
    assert exercise.equipment_needed is True
    db.session.delete(exercise)
    db.session.commit()

def test_delete_exercise(client):
    response = client.post("/exercises",json={
        "name":"Mountain climb",
        "category":"cardio",
        "equipment_needed":False
    })
    exercise_id = response.get_json()["id"]
    response =client.delete(f"/exercises/{exercise_id}")
    assert response.status_code == 200

def test_get_all_workouts(client):
    response = client.get("/workouts")
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data,list)

def test_workout_and_exercises(client):
    response = client.get("/workouts/1")
    data =response.get_json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert "date" in data
    assert "duration_minutes" in data
    assert "notes" in data
    assert "exercises" in data

    assert isinstance(data["exercises"],list)