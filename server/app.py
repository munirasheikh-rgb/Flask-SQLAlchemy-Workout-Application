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

@app.route("/exercises",methods=["GET"])
def view_exercises():
    exercises = Exercise.query.all()
    return jsonify([{
        "id":exercise.id,
        "name":exercise.name,
        "category":exercise.category,
        "equipment_needed":exercise.equipment_needed
    }for exercise in exercises]),200

if __name__ == '__main__':
    app.run(port=5555, debug=True)