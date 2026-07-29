# Workout Tracker REST API 
## Project Description
A Flask REST API for managing reusable exercises,workouts and the exercises assigned to each workout.
The Application uses Flask SQLAlchemy for database management ,Flask Migrate for migrations, Marshmallow for serialization,deserialization and validation of data and pytest for testing

## Features 
- Create and view all exercises
- View an exercise with its associated workouts
- Delete an exercise and related workout-exercises records
- Create and view all workouts
- View a workout with its associated exercises
- Delete a workout and related exercises
- Add an exercise to workout including reps,sets and duration
- Validate incoming requests data using marshamallow
- Serialize and Deserialize data in the best format(JSON) using marshmallow
- Seed the database with sample data
- Test API endpoints using pytest

## Technologies Used 
- Python
- flask
- Flask SQLAlchemy
- Flask-migrate
- Flask-marshmallow
- Marshmallow 
- SQLite
- pytest

## Project Structure
```text
server/
|-- app.py
|-- models.py
|-- schemas.py
|-- seed.py
|-- migrations/
|-- instance/
|-- tests/
|-- test_app.py
```
## Installation 
- Clone the repository 
```bash
git clone https://github.com/munirasheikh-rgb/Flask-SQLAlchemy-Workout-Application.git
```
- Navigate to the project directory
```bash
cd Flask-SQLAlchemy-Workout-Application
```
- Install the dependencies and activate the python environment 
```bash
pipenv install
pipenv shell
```
- Navigate to the server directory where the app runs
```bash
cd server
```
- Initialize and apply database migrations
```bash
flask db init
flask db migrate -m "migration message"
flask db upgrade head
```
- Seed the database
```
python seed.py
```
## Run the Application
- Inside the server directory, run:
```text
python app.py
````
- The API runs at:
```bash
http://127.0.0.1:5555
```
## API Endpoints
### Home
GET/
- Returns a welcome message
### Exercises
GET/exercises
- Returns all exercises

GET/exercises/id
- Returns a single exercise with its related workouts.

POST/exercises
- Creates or Add a new exercise

DELETE/exercises/id
- Deletes an exercise with its associated workout-exercise records

### Workouts
GET/workouts
- Returns all workouts

GET/workouts/id
- Returns a single workout with its related exercises.

POST/workouts
- Creates or Add a new workout

DELETE/workouts/id
- Deletes a workout with its associated workout-exercise records.

### WorkoutExercise
POST/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises
- Adds an existing exercise to an existing workout including the reps,sets and duration

## Running tests
```bash
python -m pytest
```
## Dependencies
All project dependencies are listed in the pipfile, install them by running:
```bash
pipenv install
``` 
