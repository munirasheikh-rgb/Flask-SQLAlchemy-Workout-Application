from flask import Flask,jsonify,request
from flask_migrate import Migrate
from marshmallow import ValidationError
from models import db,Exercise,Workout,WorkoutExercise
from schemas import ma
from schemas import(exercise_schema ,exercises_schema,workouts_schema,
                    workout_schema,w_exercise_schema,) 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

ma.init_app(app) 

# define home/index  route
@app.route("/",methods=["GET"])
def index():
    return "<h3>Welcome to the workout tracker app!</h3>"
 
# retrieve all exercises from db
@app.route("/exercises",methods=["GET"])
def view_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)),200

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
        data = exercise_schema.load(request.get_json() or {})
        new_exercise = Exercise(name=data["name"],category=data["category"],equipment_needed=data.get("equipment_needed",False))
        # save new exercise to the db
        db.session.add(new_exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(new_exercise)),201
    
    except ValidationError as e:
        db.session.rollback()
        return jsonify({"error":e.messages}),400
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
    return jsonify(workouts_schema.dump(workouts)),200

@app.route("/workouts/<int:id>",methods=["GET"])
def workout_and_exercises(id):
    workout = db.session.get(Workout,id)

    if not workout:
        return jsonify({"error":"Workout not found!"}),404
    else:
        return jsonify({
            "id":workout.id,
            "date":workout.date.isoformat(),
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
    
    #Add new workout 
@app.route("/workouts",methods=["POST"])
def create_workout():
 try:
    data =workout_schema.load(request.get_json() or {})

    if data is None:
        return jsonify({"error":"Request body must contain JSON data"}),400

    new_workout = Workout(date=data["date"],duration_minutes=data["duration_minutes"],notes=data.get("notes"))
    # save new workout 
    db.session.add(new_workout)
    db.session.commit()
    # serialize saved workout into JSON dictionary
    return jsonify(workout_schema.dump(new_workout)),201
 
 except ValidationError as e:
     db.session.rollback()
     return jsonify({"error":e.messages}),400
     
 except(ValueError,KeyError,TypeError) as e:
    db.session.rollback()
    return jsonify({"error":str(e)}),400
 
# delete work out related to exercises
@app.route("/workouts/<int:id>",methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout,id)

    if not workout:
        return jsonify({"error":"Workout not found"}),404
    try:
        db.session.delete(workout)
        db.session.commit()
        return jsonify({"message":"Workout deleted successfully"}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),400
# add new exercise to a workout with optional sets,reps,and duration_seconds
@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",methods=["POST"])
def create_workout_exercises(workout_id,exercise_id):
    # retrieve workout and exercise from the db
    workout = db.session.get(Workout,workout_id)
    exercise = db.session.get(Exercise,exercise_id)
    # return an error if workout or exercise do not exist
    if workout is None:
        return jsonify({"error":"Workout not found."}),404
    if exercise is None:
        return jsonify({"error":"Exercise not found."}),404

    try:
        # deserialize and validate incoming new_w_exercise data
        data = w_exercise_schema.load(request.get_json() or {})
        new_w_exercise = WorkoutExercise(workout_id=workout_id,
                                         exercise_id=exercise_id,
                                         reps=data.get("reps"),
                                         sets= data.get("sets"),
                                         duration_seconds=data.get("duration_seconds"))
        db.session.add(new_w_exercise)
        db.session.commit()
        # serialize the new_w_exercise into JSON ready dictionary
        return jsonify(w_exercise_schema.dump(new_w_exercise)),201
    
    except ValidationError as e:
        db.session.rollback()
        return jsonify({"error":e.messages}),400

    except(ValueError,TypeError) as e:
        # revert back the transaction if validation fails
        db.session.rollback()
        return jsonify({"error":str(e)}),400
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)