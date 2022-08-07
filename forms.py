from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Optional, AnyOf,URL,NumberRange



class AddPetForm(FlaskForm):
    """A form for adding pets"""
    pet_name = StringField("Pet Name",validators=[InputRequired()])
    species = StringField("Species",validators=[InputRequired(),AnyOf(['Cat','Dog','Porcupine'],message='Species must be either a Cat, Dog, or Porcupine!')])
    photo_url = StringField('Photo URL',validators=[Optional()])
    age  = IntegerField('Pet Age',validators=[Optional(),NumberRange(min=0,max=30)])
    notes = StringField('Notes',validators=[Optional()])


class EditPetForm(FlaskForm):
    """A form for editing pets"""
    photo_url = StringField('Photo URL',validators=[Optional(),URL()])
    notes = StringField('Notes',validators=[Optional()])
    is_available = BooleanField('Available',validators=[Optional()])
