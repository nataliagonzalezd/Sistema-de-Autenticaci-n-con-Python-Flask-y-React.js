"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json, session
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Characters, Planets, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(), allusers))

    return jsonify(results), 200

@app.route('/favorites', methods=['GET'])
def handle_favorites():
    allfavorites = Favorites.query.all()
    favorites = list(map(lambda item: item.serialize(), allfavorites))

    return jsonify(favorites), 200

@app.route('/characters', methods=['GET'])
def handle_characters():
    allcharacters = Characters.query.all()
    characters = list(map(lambda item: item.serialize(), allcharacters))

    return jsonify(characters), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_info_character(character_id):

    character = Characters.query.filter_by(id=character_id).first()
    print(character)

    return jsonify(character.serialize()), 200


@app.route('/planets', methods=['GET'])
def handle_planets():
    allplanets = Planets.query.all()
    planets = list(map(lambda item: item.serialize(), allplanets))

    return jsonify(planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_info_planet(planet_id):

    planet = Planets.query.filter_by(id=planet_id).first()

    return jsonify(planet.serialize()), 200

@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    allvehicles = Vehicles.query.all()
    vehicles = list(map(lambda item: item.serialize(), allvehicles))

    return jsonify(vehicles), 200

@app.route('/user', methods=['POST'])
def add_user():
    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(),allusers))
    request_body = json.loads(request.data)
    results.append(request_body)
    return jsonify(results), 200
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
