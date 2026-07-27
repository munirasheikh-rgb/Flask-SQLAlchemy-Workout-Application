from flask_marshmallow import Marshmallow
from marshmallow import fields ,Schema

ma = Marshmallow()

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category =fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes =fields.Int(required=True)
    notes = fields.Str(allow_none=True)
    

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id =fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets=fields.Int(allow_none=True)
    duration__seconds=fields.Int(allow_none=True)