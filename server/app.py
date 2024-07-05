#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    if 'name' not in data or 'price' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    new_plant = Plant(
        name=data['name'],
        image=data.get('image'),
        price=float(data['price'])  # Ensure price is converted to float
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict()), 201

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get_or_404(plant_id)
        return jsonify(plant.to_dict())
    
@app.route('/plants/<int:plant_id>')
def get_plant_by_id(plant_id):
    plant = db.session.get(Plant, plant_id)
    if plant is None:
        return jsonify({"error": "Plant not found"}), 404
    return jsonify(plant.to_dict()), 200


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
