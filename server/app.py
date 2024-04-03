from flask import Flask, make_response
from models import db, Earthquake
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = None

db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(json.dumps(body), 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # Query the database to get the earthquake by ID
    earthquake = Earthquake.query.get(id)

    if earthquake is not None:
        # If earthquake exists, return its attributes as JSON
        body = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        return make_response(json.dumps(body), 200)
    else:
        # If earthquake does not exist, return error message with 404 status
        body = {"message": f"Earthquake {id} not found."}
        return make_response(json.dumps(body), 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query the database to get earthquakes with magnitude greater than or equal to the parameter value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Count the number of matching earthquakes
    count = len(earthquakes)

    # Create a list containing data for each matching earthquake
    quakes = []
    for earthquake in earthquakes:
        quake_data = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        quakes.append(quake_data)

    # Create JSON response
    response_data = {
        "count": count,
        "quakes": quakes
    }

    return make_response(json.dumps(response_data), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
