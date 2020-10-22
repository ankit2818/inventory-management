from flask_wtf import FlaskForm
from datetime import datetime, date
from wtforms.fields import StringField, SelectField,SubmitField, DateField
from wtforms_components import DateRange, widgets
from wtforms.validators import DataRequired




class ProductForm(FlaskForm):
    productName = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField("Save Product")

class LocationForm(FlaskForm):
    locationName = StringField('Location Name', validators=[DataRequired()])
    locationAddress = StringField('Location Address', validators=[DataRequired()])
    submit = SubmitField("Save Location")

class ProductMovementForm(FlaskForm):
    date = StringField('Date of Movement', validators=[DataRequired()], widget=widgets.DateInput())
    fromLocation = SelectField('Select From Location', default=None)
    toLocation = SelectField('Select To Location', default=None)
    productName = SelectField('Select Product', validators=[DataRequired()])
    productQuantity = SelectField('Enter Product Quantity', choices=[i for i in range(1, 1000)], validators=[DataRequired()], default=1)
    submit = SubmitField("Save Product Movement")
