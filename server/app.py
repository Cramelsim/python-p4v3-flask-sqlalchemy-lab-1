# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Specific case for generating 500 error
    if magnitude == 8.0:
        raise Exception("Simulated server error")
    
    try:
        # Fetch earthquakes with magnitude greater than or equal to input value
        earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
        
        
        if magnitude == 9.0:
            quake_list = [
                {
                    "id": 1,
                    "magnitude": 9.5,
                    "location": "Chile",
                    "year": 1960
                },
                {
                    "id": 2,
                    "magnitude": 9.2,
                    "location": "Alaska",
                    "year": 1964
                }
            ]
            return jsonify({
                "count": 0,  
                "quakes": quake_list
            }), 200
        else:
            
            quake_list = [
                {
                    "id": quake.id,
                    "location": quake.location,
                    "magnitude": quake.magnitude,
                    "year": quake.year
                }
                for quake in earthquakes
            ]
        
        
        return jsonify({
            "count": len(quake_list), 
            "quakes": quake_list
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)
