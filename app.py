"""Blogly application."""

from flask import *
from models import *
from forms import AddPetForm, EditPetForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "catsarethebest"

connect_db(app)
db.create_all()


@app.route("/")
def show_home_page():
    """lists all pets on the home page"""
    pets = Pet.query.all()
    return render_template("home_page.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def show_add_pet():
    """show form or add a pet"""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.pet_name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        new_pet = Pet(
            name=name, species=species, photo_url=photo_url, age=age, notes=notes
        )

        db.session.add(new_pet)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("add_pet_form.html", form=form)


@app.route("/pet/<int:pet_id>", methods=["GET", "POST"])
def show_pet(pet_id):
    """shows a pet and the form to edit the pet"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data if form.photo_url.data else pet.photo_url
        pet.notes = form.notes.data if form.notes.data else pet.notes
        pet.is_available = form.is_available.data

        db.session.add(pet)
        db.session.commit()
        return redirect(f"/pet/{pet_id}")
    else:
        return render_template("edit_pet_form.html", form=form, current_pet=pet)


@app.route("/pets/available")
def show_available_pets():
    """lists all available pets on the home page"""
    pets = Pet.query.filter_by(is_available=True).all()
    return render_template("home_page.html", pets=pets)


@app.route("/pets/adopted")
def show_adopted_pets():
    """lists all adopted pets on the home page"""
    pets = Pet.query.filter_by(is_available=False).all()
    return render_template("home_page.html", pets=pets)
