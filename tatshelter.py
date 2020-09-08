import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddForm, AdoptForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

#############################
########## SQL DB ###########
#############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

#############################
######### MODELS ############
#############################

class Owner(db.Model):
    
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    full_name = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    owned = db.relationship('Pet', backref='owner', lazy='dynamic')

    def __init__(self, full_name, email, phone_number):
        self.email = email
        self.full_name = full_name
        self.phone_number = phone_number

class Adopter(db.Model):
    
    __tablename__ = 'adopters'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    full_name = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    adopted = db.relationship('Pet', backref='adopter', lazy='dynamic')

    def __init__(self, full_name, email, phone_number):
        self.email = email
        self.full_name = full_name
        self.phone_number = phone_number

class Pet(db.Model):

    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    pet_type = db.Column(db.Text)
    age = db.Column(db.Integer)
    info = db.Column(db.Text)
    adopted = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    adopter_id = db.Column(db.Integer, db.ForeignKey('adopters.id'))
    pic = db.Column(db.String(64))

    def __init__(self, name, pet_type, age, info, owner_id):
        self.name = name
        self.pet_type = pet_type
        self.age = age
        if info:
            self.info = info
        else:
            self.info = ""
        self.owner_id = owner_id
        self.adopter_id = owner_id
        self.adopted = False


#############################
########## VIEWS ############
#############################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_pets')
def list_pets():
    pets = Pet.query.all()
    return render_template('list_pets.html', pets = pets)

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    form = AddForm()

    if form.validate_on_submit():
        # create owner
        owner_name = form.owner_name.data
        owner_email = form.owner_email.data
        owner_phone = form.owner_phone.data
        owner = Owner.query.filter_by(email=owner_email).first()
        if owner is None:
            owner = Owner(owner_name, owner_email, owner_phone)
            db.session.add(owner)
            db.session.commit()
            owner = Owner.query.filter_by(email=owner_email).first()

        # create pet
        pet_name = form.pet_name.data
        pet_type = form.pet_type.data
        pet_age = form.pet_age.data
        pet_info = form.additional.data
        pet = Pet(pet_name, pet_type, pet_age, pet_info, owner.id)
        db.session.add_all([pet, owner])
        db.session.commit()

        return redirect(url_for('list_pets'))
    
    return render_template('add_pet.html', form=form)

@app.route('/pet/<pet_id>', methods=['GET', 'POST'])
def pet(pet_id):
    pet_id = int(pet_id)
    pet = Pet.query.get(pet_id).first()

    form = AdoptForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        adopter = Adopter.query.filter_by(email=email).first()
        if adopter is None:
            adopter = Adopter(name, email, phone)
            db.session.add(adopter)
            db.session.commit()
            adopter = Adopter.query.filter_by(email=email).first()
        pet.adopted = True
        pet.adopter_id = adopter.id
        db.session.add_all([adopter, pet])
        db.session.commit()

        return redirect(url_for('list_pets'))

    return render_template('pet.html', form=form, pet=pet)

if __name__ == '__main__':
    app.run(debug=True)