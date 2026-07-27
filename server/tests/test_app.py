import pytest 
from app import app
from datetime import date
from models import db,Exercise,Workout,WorkoutExercise

@pytest.fixture
def client():
    app.config["TESTING"] =True
    with app.app_context():
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

def test_create_workout(client):
    workout = None
    try:
     response =client.post("/workouts", json={
         "date":"2026-07-27",
         "duration_minutes":30,
         "notes":"full body session workout"
     })
     data = response.get_json()
     assert response.status_code == 201

     workout = db.session.get(Workout,data["id"])
     assert workout is not None
     assert workout.date.isoformat() == "2026-07-27"
     assert workout.duration_minutes == 30
     assert workout.notes == "full body session workout"

    finally:
        if workout is not None:
            db.session.delete(workout)
            db.session.commit()

def test_adds_exercise_to_workout(client):
    workout = Workout(date=date(2026,6,24),duration_minutes=40,notes="test workout notes")
    exercise = Exercise(name="squats",category="flexibility",equipment_needed=False)
    db.session.add_all([workout,exercise])
    db.session.commit()

    try:
     response = client.post(f"/workouts/{workout.id}/exercises/{exercise.id}/workout_exercises",
                            json={"reps":5,"sets":2,"duration_seconds":1000})
     data = response.get_json()
     assert response.status_code == 201
     assert data["workout_id"] == workout.id
     assert data["exercise_id"] == exercise.id
     assert data["reps"] == 5
     assert data["sets"] == 2
     assert data["duration_seconds"] == 1000

     workout_exercise = db.session.get(WorkoutExercise,data["id"])
     assert workout_exercise is not None
     assert workout_exercise.workout_id == workout.id
     assert workout_exercise.exercise_id== exercise.id
    finally:
        WorkoutExercise.query.filter_by(workout_id=workout.id,exercise_id=exercise.id).delete()
        db.session.delete(workout)
        db.session.delete(exercise)
        db.session.commit()

