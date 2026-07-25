from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from datetime import date
metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

#Exercise model stores reusable exercises
class Exercise(db.Model):
    __tablename__= "exercises"

    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String,nullable=False)
    category= db.Column(db.String,nullable=False)
    equipment_needed = db.Column(db.Boolean,nullable=False,default=False)

# one exercise belongs to many workouts
    workout_exercises = db.relationship("WorkoutExercise",back_populates="exercise",cascade="all, delete-orphan")
# validate exercise name
    @validates("name") 
    def validate_name(self,value):
        if not value or not value.strip():
            raise ValueError("Exercise name is required.")

        cleaned_value = value.strip()
        if len(cleaned_value) < 2:
            raise ValueError("Exercise must contain 2 or more characters.")
        return cleaned_value
# validate exercise category
    @validates("category")
    def validate_category(self,value):
        categories_allowed = {
            "cardio",
            "flexibility",
            "pilates",
            "balance",
            "weight lift",
            "yoga",
            "cycle",
            "running"
        }

        if not value or not value.strip():
            raise ValueError("Exercise category is required")
        cleaned_value = value.strip().lower()
        if cleaned_value not in categories_allowed:
            raise ValueError(f"categories must be:"f"{','.join(sorted(categories_allowed))}")
        return cleaned_value
  # workout model stores workout sessions
class Workout(db.Model):
    __tablename__="workouts"
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.Date,nullable=False,default=date.today)
    duration_minutes = db.Column(db.Integer,nullable=False)
    notes = db.Column(db.String)

# one workout contains many exercises
    workout_exercises = db.relationship("WorkoutExercise",back_populates="workout",cascade="all, delete-orphan")

# validate workout duration
    @validates("duration_minutes")
    def validate_duration(self,value):
      if value is None:
          raise ValueError("Workout duration is required.")
      if value <= 0 :
          raise ValueError("workout duration must be greater than zero!")
      if value >1440:
          raise ValueError("workout duration cannot exceed 1440 minutes")
      else:
          return value

    # validate workout notes
    @validates("notes")
    def validate_notes(self,value):
        if value is not None and len(value) > 500:
            raise ValueError("notes should not exceed 500 characters")
        return value
    
 # model linking workout and exercises
class WorkoutExercise(db.Model):
    __tablename__="workout_exercises"
    id = db.Column(db.Integer,primary_key=True)
    workout_id = db.Column(db.Integer,db.ForeignKey("workouts.id"),nullable=False)
    exercise_id = db.Column(db.Integer,db.ForeignKey("exercises.id"),nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

# relationships
    workout = db.relationship("Workout",back_populates="workout_exercises")
    exercise = db.relationship("Exercise",back_populates="workout_exercises")

# validate values are positive integers
    @validates("duration_seconds","reps","sets")
    def validate_positive_numbers(self,key,value):
        if value is not None and value <= 0 :
            raise ValueError(f"{key} must be greater than zero")
        return value