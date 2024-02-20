# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

@app.route("/pets/<int:id>")
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    # doesn't work without the '.first()'... why?
    # pet = Pet.query.filter(Pet.id == id)

    if pet:
        body = pet.to_dict(only=("name", "species"))
        status = 200
    else:
        body = {"message": f"Pet {id} not found."}
        status = 404

    return make_response(body, status)


    
@app.route("/pets/<string:species>")
def pet_by_species(species):
    pets = []
    for pet in Pet.query.filter(Pet.species == species).all():
        pets.append(pet.to_dict(only=("name", "species")))
    return make_response({"count": len(pets), "pets": pets}, 200)
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
