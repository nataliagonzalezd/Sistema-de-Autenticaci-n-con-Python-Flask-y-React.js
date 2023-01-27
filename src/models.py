from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(250), nullable=False)
    lastName = db.Column(db.String(250), nullable=False)
    userName = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorites', backref='User',lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "userName": self.userName,
            "favorties": self.favorites,
        }


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    planets_favorites = db.Column(db.Integer, db.ForeignKey('planets.id'),nullable=True)
    vehicles_favorites = db.Column(db.Integer, db.ForeignKey('vehicles.id'),nullable=True)
    characters_favorites = db.Column(db.Integer, db.ForeignKey('characters.id'),nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_favorites": self.planets_favorites,
            "vehicles_favorites": self.vehicles_favorites,
            "characters_favorites": self.characters_favorites,
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    height = db.Column(db.String(250))
    mass = db.Column(db.String(250))
    hairColor = db.Column(db.String(250))
    skinColor = db.Column(db.String(250))
    eyeColor = db.Column(db.String(250))
    birthYear = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    homeworld = db.Column(db.Integer,db.ForeignKey('planets.id')) 
    films = db.Column(db.String(250))
    species = db.Column(db.String(250))
    vehiclespilots = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    starships = db.Column(db.String(250))
    created = db.Column(db.String(250))
    edited = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='characters',lazy=True)


    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "haircolor": self.hairColor,
            "skincolor": self.skinColor,
            "eyecolor": self.eyeColor,
            "birthyear": self.birthYear,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "films": self.films,
            "species": self.species,
            "vehicles": self.vehiclespilots,
            "starships": self.starships,
            "created": self.created,
            "edited": self.edited,
        }
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),nullable=False)
    favorites = db.relationship('Favorites', backref='planets',lazy=True)
    climate = db.Column(db.String(250))
    created = db.Column(db.String(250))
    diameter = db.Column(db.String(250))
    edited = db.Column(db.String(250))
    films = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    orbitalperiod = db.Column(db.String(250))
    population = db.Column(db.String(250))
    residents = db.relationship('Characters', lazy='select', backref=db.backref('planets', lazy='joined'))
    rotationperiod = db.Column(db.String(250))
    surfacewater = db.Column(db.String(250))
    terrain = db.Column(db.String(250))


    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "created": self.created,
            "diameter": self.diameter,
            "edited": self.edited,
            "films": self.films,
            "gravity": self.gravity,
            "orbitalPeriod": self.orbitalperiod,
            "population": self.population,
            "rotationperiod": self.rotationperiod,
            "surfacewater": self.surfacewater,
            "terrain": self.terrain,
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='Vehicles',lazy=True)
    cargocapacity = db.Column(db.String(250))
    consumables = db.Column(db.String(250))
    costincredits = db.Column(db.String(250))
    crew = db.Column(db.String(250))
    edited = db.Column(db.String(250))
    length = db.Column(db.String(250))
    manufactured = db.Column(db.String(250))
    maxatmspeed = db.Column(db.String(250))
    model = db.Column(db.String(250))
    passengers = db.Column(db.String(250))
    pilots = db.relationship('Characters', lazy='select',
        backref=db.backref('vehicles', lazy='joined'))
    films = db.Column(db.String(250))
    vehicleclass = db.Column(db.String(250))

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cargocapacity": self.cargocapacity,
            "consumables" : self.consumables,
            "costincredits": self.costincredits,
            "crew": self.crew,
            "edited": self.edited,
            "lenght": self.length,
            "manufactered": self.manufactured,
            "maxatmspeed": self.maxatmspeed,
            "model": self.model,
            "passengers": self.passengers,
            "films": self.films,
            "vehicleclass": self.vehicleclass,
        }