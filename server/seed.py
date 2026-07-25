from app import app
from models import db, Exercise,Workout, WorkoutExercise
from datetime import date

with app.app_context():

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    exercise1 = Exercise(name="push-ups",category="balance",equipment_needed=False)
    exercise2 = Exercise(name="Tread_mill running",category="cardio",equipment_needed=True)
    exercise3 = Exercise(name="leg stretches",category="pilates",equipment_needed=False)
    exercise4 = Exercise(name="bicycle riding",category="cycle",equipment_needed=True)

    db.session.add_all([exercise1,exercise2,exercise3,exercise4])
    db.session.commit()


    workout1 = Workout(date=date(2026,7,20),duration_minutes=30,notes="Cardio and lower body session")
    workout2 =  Workout(date=date(2026,7,22),duration_minutes=45,notes="Upper-body and glutes session")
    workout3 = Workout(date=date(2026,7,26),duration_minutes=20,notes="Core and yoga sessions")

    db.session.add_all([workout1,workout2,workout3])
    db.session.commit()


    workout_exercise1 = WorkoutExercise(workout_id= workout1.id,exercise_id=exercise2.id,reps=8,sets=4,duration_seconds=1000)
    workout_exercise2 = WorkoutExercise(workout_id= workout2.id,exercise_id=exercise3.id,reps=6,sets=2,duration_seconds=1500)
    workout_exercise3= WorkoutExercise(workout_id= workout3.id,exercise_id=exercise4.id,duration_seconds=1000)
    workout_exercise4 = WorkoutExercise(workout_id= workout2.id,exercise_id=exercise1.id,reps=11,duration_seconds=3000)

    db.session.add_all([workout_exercise1,workout_exercise2,workout_exercise3,workout_exercise4])
    db.session.commit()