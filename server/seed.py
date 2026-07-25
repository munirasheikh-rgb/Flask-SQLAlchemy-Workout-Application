from app import app
from models import db, Exercise,Workout, WorkoutExercise

with app.app_context():

    exercise1 = Exercise(name="push-ups",category="balance",equipment_needed=False)
    exercise2 = Exercise(name="Tread_mill running",category="cardio",equipment_needed=True)
    exercise3 = Exercise(name="leg stretches",category="pilates",equipment_needed=False)
    exercise4 = Exercise(name="bicycle riding",category="cycle",equipment_needed=True)

    db.session.add_all([exercise1,exercise2,exercise3,exercise4])
    db.session.commit()
