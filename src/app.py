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

# [GET] /users

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

# [GET] /people

@app.route('/characters', methods=['GET'])
def handle_characters():
    allcharacters = Characters.query.all()
    characters = list(map(lambda item: item.serialize(), allcharacters))

    return jsonify(characters), 200

# [GET] /people/<int:people_id>

@app.route('/character/<int:character_id>', methods=['GET'])
def get_info_character(character_id):

    character = Characters.query.filter_by(id=character_id).first()
    print(character)

    return jsonify(character.serialize()), 200

# [GET] /planets

@app.route('/planets', methods=['GET'])
def handle_planets():
    allplanets = Planets.query.all()
    planets = list(map(lambda item: item.serialize(), allplanets))

    return jsonify(planets), 200

# [GET] /planets/<int:planet_id>

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_info_planet(planet_id):

    planet = Planets.query.filter_by(id=planet_id).first()

    return jsonify(planet.serialize()), 200


@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    allvehicles = Vehicles.query.all()
    vehicles = list(map(lambda item: item.serialize(), allvehicles))

    return jsonify(vehicles), 200

# [GET] /users/favorites

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def handle_favoritesuser(user_id):
    favoritesuser = Favorites.query.filter_by(user_id=user_id).all()
    favoritesselected = list(map(lambda item: item.serialize(), favoritesuser))

    return jsonify(favoritesselected), 200

# [POST] /user

@app.route('/user', methods=['POST'])
def add_user():
    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(),allusers))
    request_body = json.loads(request.data)
    results.append(request_body)
    return jsonify(results), 201

# [POST] /favorite/planet/<int:planet_id>

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.filter_by(id=user_id).first()
    planet = Planets.query.filter_by(id=planet_id).first()
    favorite = Favorites(user_id=user.id, planets_favorites=planet.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

# [POST] /favorite/people/<int:people_id>

@app.route('/favorites/user/<int:user_id>/characters/<int:characters_id>', methods=['POST'])
def add_favorite_character(user_id, characters_id):
    user = User.query.filter_by(id=user_id).first()
    characters = Characters.query.filter_by(id=characters_id).first()
    favorite = Favorites(user_id=user.id, characters_favorites=characters.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

# [DELETE] /favorite/planet/<int:planet_id>

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favoriteplanet = Favorites.query.filter_by(user_id=user_id, planets_favorites=planet_id).first()
    db.session.delete(favoriteplanet)
    db.session.commit()

    return jsonify("Done"), 200

# [DELETE] /favorite/people/<int:people_id>

@app.route('/favorite/user/<int:user_id>/characters/<int:characters_id>', methods=['DELETE'])
def delete_favorite_character(user_id, characters_id):
    favoritesch = Favorites.query.filter_by(user_id=user_id).filter_by(characters_favorites=characters_id).first()
    db.session.delete(favoritesch)
    db.session.commit()

    return jsonify("Done"), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
