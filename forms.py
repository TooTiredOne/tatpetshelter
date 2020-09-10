from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, Optional
from flask_wtf.file import FileAllowed, FileField

class AddForm(FlaskForm):

    pet_name = StringField('Name of the pet: ', [InputRequired(message="Please, provide pet name")])
    pet_type = StringField('Pet type: ', [InputRequired(message="Please, provide pet type")])
    pet_age = IntegerField('Pet age (in years): ', [InputRequired(message="Please, provide pet age"), NumberRange(0, 100)])
    additional = TextAreaField('Additional information: ')
    owner_name = StringField('Owner name: ', [InputRequired(message="Please, provide owner name")])
    owner_email = StringField('Contact email: ', [InputRequired(message="Please, provide owner contact email")])
    owner_phone = StringField('Phone number: ', [InputRequired(message="Please, provide owner contact phone")])
    pet_pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg']), Optional()])
    submit = SubmitField('Add pet')

class AdoptForm(FlaskForm):
    name = StringField('Adopter name: ', [InputRequired(message="Please, provide adopter name")])
    email = StringField('Contact email: ', [InputRequired(message="Please, provide adopter contact email")])
    phone = StringField('Phone number: ', [InputRequired(message="Please, provide adopter contact phone")])
    submit = SubmitField('Adopt that pet')