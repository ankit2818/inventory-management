from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    productName = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField("Save Product")

class LocationForm(FlaskForm):
    locationName = StringField('Location Name', validators=[DataRequired()])
    locationAddress = StringField('Location Address', validators=[DataRequired()])
    submit = SubmitField("Save Location")