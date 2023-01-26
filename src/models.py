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
    name = db.Column(db.String(250))
    planets_Id = db.relationship('Planets', backref='Favorites',lazy=True)
    vehicles_Id = db.relationship('Vehicles', backref='Favorites',lazy=True)
    characters_Id = db.relationship('Characters', backref='Favorites',lazy=True)
    user_Id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_Id": self.user_Id,
            "planets_Id": self.planets_Id,
            "vehicles_Id": self.vehicles_Id,
            "characters_Id": self.characters_Id,
        }

class Characters(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('favorites.id'), primary_key=True)
    name = db.Column(db.String(250))
    url = db.Column(db.String(250))
    # details_ID = db.relationship('CharactersDetails', backref='Characters',lazy=True)


    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "details_ID": self.details_ID,
        }


class Planets(db.Model):
    name = db.Column(db.String(250))
    url = db.Column(db.String(250))
    # details_ID = db.relationship('CharactersDetails', backref='Planets',lazy=True)
    id = db.Column(db.Integer, db.ForeignKey('favorites.id'), primary_key=True)


    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "details_ID": self.details_ID,
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('favorites.id'), primary_key=True)
    name = db.Column(db.String(250))
    url = db.Column(db.String(250))
    # details_ID = db.relationship('CharactersDetails', backref='Vehicles',lazy=True)

    
    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "details_ID": self.details_ID,
        }

# class CharactersDetails(db.Model):
#     planets = db.Column(db.Integer, db.ForeignKey('planets.id'),nullable=True)
#     vehicles = db.Column(db.Integer, db.ForeignKey('vehicles.id'),nullable=True)
#     id = db.Column(db.Integer, db.ForeignKey('characters.id'), primary_key=True)
#     height = db.Column(db.String(250))
#     mass = db.Column(db.String(250))
#     hairColor = db.Column(db.String(250))
#     skinColor = db.Column(db.String(250))
#     eyeColor = db.Column(db.String(250))
#     birthYear = db.Column(db.String(250))
#     gender = db.Column(db.String(250))
#     homeworld = db.Column(db.String(250),db.ForeignKey('planets.url'))
#     films = db.Column(db.String(250))
#     species = db.Column(db.String(250))
#     vehicles = db.Column(db.String(250), db.ForeignKey('vehicles.url'))
#     starships = db.Column(db.String(250))
#     created = db.Column(db.String(250))
#     edited = db.Column(db.String(250))

#     def __repr__(self):
#         return '<CharactersDetails %r>' % self.id

#     def serialize(self):
#         return {
#             "characters": self.characters,
#             "planets": self.planets,
#             "vehicles": self.vehicles,
#             "id": self.id,
#             "height": self.height,
#             "mass": self.mass,
#             "haircolor": self.hairColor,
#             "skincolor": self.skinColor,
#             "eyecolor": self.eyeColor,
#             "birthyear": self.birthYear,
#             "gender": self.gender,
#             "homeworld": self.homeworld,
#             "films": self.films,
#             "species": self.species,
#             "vehicles": self.vehicles,
#             "starships": self.starships,
#             "created": self.created,
#             "edited": self.edited,
#         }