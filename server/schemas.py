from flask_marshmallow import Marshmallow
from marshmallow import fields ,Schema,validates,ValidationError

ma = Marshmallow()

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category =fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)
# validate exercise name
    @validates("name")
    def validate_name(self,value):
        if not value or not value.strip():
            raise ValidationError("Exercise name is required")
        
        cleaned_value = value.strip()
        if len(cleaned_value) < 2:
            raise ValidationError("Exercise must contain 2 or more characters")
# validate exercise caegory
    @validates("category")    
    def validate_category(self,value):
        allowed_c = {
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
                 raise ValidationError("Exercise category required")
                
        cleaned_value = value.strip().lower()
        if cleaned_value not in allowed_c:
            raise ValidationError(f"categories must be:"f"{','.join(sorted(allowed_c))}") 
        
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes =fields.Int(required=True)
    notes = fields.Str(allow_none=True)
# validate notes are less than 500 characters
    @validates("notes")
    def validate_notes(self,value):
        if value is not None and len(value) > 500:
            raise ValidationError("notes should'nt exceed 500 characters")

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id =fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets=fields.Int(allow_none=True)
    duration_seconds=fields.Int(allow_none=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

w_exercise_schema = WorkoutExerciseSchema()
w_exercises_schema = WorkoutExerciseSchema(many=True)


