from flask import Flask,jsonify,request,make_response
from flask_migrate import Migrate

from models import db,Exercise,Workout,WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)



# define home/index  route
@app.route("/",methods=["GET"])
def index():
    return "<h3>Welcome to the workout tracker app!</h3>"
 
# retrieve all exercises from db
@app.route("/exercises",methods=["GET"])
def view_exercises():
    exercises = Exercise.query.all()
    return jsonify([{
        "id":exercise.id,
        "name":exercise.name,
        "category":exercise.category,
        "equipment_needed":exercise.equipment_needed
    }for exercise in exercises]),200


@app.route("/exercises/<int:id>",methods=["GET"])
def get_exercise_and_workouts(id):
    exercise = db.session.get(Exercise,id)
    if exercise is None:
        return jsonify({
            'error':'Exercise not found'
        }),404
    else:
      return jsonify({
          "id":exercise.id,
          "name":exercise.name,
          "category":exercise.category,
          "equipment_needed":exercise.equipment_needed,

          "workouts":[{
              "id":we.workout.id,
              "date":we.workout.date,
              "notes":we.workout.notes,
              "sets":we.sets,
              "reps":we.reps,
              "duration_seconds":we.duration_seconds

          }for we in exercise.workout_exercises]
      }),200
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)