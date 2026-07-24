from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from datetime import date
metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Exercise(db.Model):
    __tablename__= "exercises"

    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String,nullable=False)
    category= db.Column(db.String,nullable=False)
    equipment_needed = db.Column(db.Boolean,nullable=False,default=False)

    workout_exercises = db.relationship("WorkoutExercise",back_populates="exercises",cascade="all, delete-orphan")

    @validates("name") 
    def validate_name(self,value):
        if not value or value.strip():
            raise ValueError("Exercise name required.")
        
        if len(value.strip()) < 2:
            raise ValueError("Exercise must contain 2 or more characters.")
        return value.strip()
 
    @validates("category")
    def validate_category(self,value):
        categories_allowed = {
            "Cardio",
            "flexibility",
            "pilates",
            "balance",
            "weight lift",
            "yoga",
            "cycle"
            "Running"
        }

        if not value:
            raise ValueError("Exercise category is required")
        cleaned_value = value.strip().lower()
        if cleaned_value not in categories_allowed:
            raise ValueError(f"categories must be:"f"{','.join(sorted(categories_allowed))}")
        return cleaned_value
    
class Workout(db.Model):
    __tablename__="workouts"
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.Date,nullable=False,default=date.today)
    duration_minutes = db.Column(db.Integer,nullable=False)
    notes = db.Column(db.String)

    workout_exercises = db.relationship("WorkoutExercise",back_populates="workouts",cascade="all, delete-orphan")

class WorkoutExercise(db.Model):
    __tablename__="workout_exercises"
    id = db.Column(db.Integer,primary_key=True)
    workout_id = db.Column(db.Integer,db.ForeignKey("workouts.id"),nullable=False)
    exercise_id = db.Column(db.Integer,db.ForeignKey("exercises.id"),nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout",back_populates="workout_exercises")
    exercise = db.relationship("exercise",back_populates="workout_exercises")