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

# get a specific exercise associated with it's workouts
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
            # returning an exercise with workouts
          }for we in exercise.workout_exercises]
      }),200

# create new exercise and saves to the database
@app.route("/exercises",methods=["POST"])
def add_exercise():
    try:
        data = request.get_json()
        new_exercise = Exercise(name=data["name"],category=data["category"],equipment_needed=data.get("equipment_needed",False))
        # save new exercise to the db
        db.session.add(new_exercise)
        db.session.commit()

        return jsonify({
            "id":new_exercise.id,
            "name":new_exercise.name,
            "category":new_exercise.category,
            "equipment_needed":new_exercise.equipment_needed
        }),201
    #Roll back the tansaction on error
    except(ValueError,KeyError,TypeError)as e: 
        db.session.rollback()  

        return jsonify({"error":str(e)}),400
# delete an exercise from db
@app.route("/exercises/<int:id>",methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise,id)
    if exercise is None:
        return jsonify({"error":"Exercise not found"}),404
    try:
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({"message":"Exercise deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),400

# list all workouts in the db
@app.route("/workouts",methods=["GET"])
def view_all_workouts():
    workouts = Workout.query.all()
    return jsonify([{
        "id" :workout.id,
        "date":workout.date,
        "duration_minutes":workout.duration_minutes,
        "notes":workout.notes

     }for workout in workouts]),200

@app.route("/workouts/<int:id>",methods=["GET"])
def workout_and_exercises(id):
    workout = db.session.get(Workout,id)

    if not workout:
        return jsonify({"error":"Workout not found!"}),404
    else:
        return jsonify({
            "id":workout.id,
            "date":workout.date,
            "duration_minutes":workout.duration_minutes,
            "notes":workout.notes,

            "exercises":[{
             "id":we.exercise.id,
             "name":we.exercise.name,
             "category":we.exercise.category,
             "equipment_needed":we.exercise.equipment_needed,
             "sets":we.sets,
             "reps":we.reps,
             "duration_seconds":we.duration_seconds
             
            }for we in workout.workout_exercises]

        }),200
    
     




if __name__ == '__main__':
    app.run(port=5555, debug=True)