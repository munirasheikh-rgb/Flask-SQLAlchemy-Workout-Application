from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from datetime import date
metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Exercise(db.Model):
    __tablename__= "exercises"

    id = db.column(db.Integer,primary_key=True)
    name = db.column(db.String,nullable=False)
    category= db.column(db.String,nullable=False)
    equipment_needed = db.column(db.Boolean,nullable=False,default=False)

    workout_exercises = db.relationship("WorkoutExercise",back_populates="exercises",cascade="all ,delete_orphan")

class Workout(db.Model):
    __tablename__="workouts"
    id = db.column(db.Integer,primary_key=True)
    date = db.column(db.Date,nullable=False,default=date.today)
    duration_minutes = db.column(db.Integer,nullable=False)
    notes = db.column(db.String)

    workout_exercises = db.relationship("WorkoutExercise",back_populates="workouts",cascade="all ,delete_orphan")

class WorkoutExercise(db.Model):
    __tablename__="workout_exercises"
    id = db.column(db.Integer,primary_key=True)
    workout_id = db.column(db.Integer,db.ForeignKey("workouts.id"),nullable=False)
    exercise_id = db.column(db.Integer,db.ForeignKey("exercises.id"),nullable=False)
    reps = db.column(db.Integer)
    sets = db.column(db.Integer)
    duration_seconds = db.column(db.Integer)

    workout = db.relatioship("Workout",back_populates="workout_exercises")
    exercise = db.relatioship("exercise",back_populates="workout_exercises")