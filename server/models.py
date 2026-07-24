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

    workout_exercises = db.relationship("WorkoutExercise",back_populates="exercise",cascade="all ,delete_orphan")

class Workout(db.Model):
    __tablename__="workouts"
    id = db.column(db.Integer,primary_key=True)
    date = db.column(db.Date,nullable=False,default=date.today)
    duration_minutes = db.column(db.Integer,nullable=False)
    notes = db.column(db.String)

    workout_exercises = db.relationship("WorkoutExercise",back_populates="workout",cascade="all ,delete_orphan")


    