from flask import Flask
from flask_migrate import Migrate

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)



# Define Routes here
@app.route("/",methods=["GET"])
def index():
    return "<h3>Welcome to the workout tracker app!</h3>"



if __name__ == '__main__':
    app.run(port=5555, debug=True)