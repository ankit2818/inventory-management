from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import ProductForm, LocationForm, ProductMovementForm
from config import Config
import random


app = Flask(__name__)
app.config.from_object(Config)

# Database
db = SQLAlchemy(app)



# Import Models
from models import Product, Location, ProductMovement, Stock


# Choose Random Username
def username():
    usernameList = ["Hermione Granger", "Harry Potter", "Ron Weasley"]
    return random.choice(usernameList)


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title="Home", username=username())

# Product related routes
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', title="Products", products=products)

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(productQuantity = form.productName.data)
        db.session.add(product)
        db.session.commit()
        flash('Product has been added.', 'success')
        return redirect(url_for("products"))
    return render_template('addproduct.html', title="Products", form=form, legend = 'Add New product')

@app.route('/updateproduct/<int:productId>', methods=['GET', 'POST'])
def updateproduct(productId):
    product = Product.query.get_or_404(productId)
    form = ProductForm()
    if form.validate_on_submit():
        product.productName = form.productName.data
        db.session.commit()
        flash('Product Name has been updated.', 'success')
        return redirect(url_for("products"))
    form.productName.data = product.productName
    return render_template('addproduct.html', form=form, legend = 'Update Product')


# Location related routes
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', title="Locations", locations=locations)

@app.route('/addlocation', methods=['GET', 'POST'])
def addlocation():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(locationName = form.locationName.data, locationAddress = form.locationAddress.data)
        db.session.add(location)
        db.session.commit()
        flash('Location has been added.', 'success')
        return redirect(url_for("locations"))
    return render_template('addlocation.html', title="Locations", form=form, legend = 'Add New location')

@app.route('/updatelocation/<int:locationId>', methods=['GET', 'POST'])
def updatelocation(locationId):
    location = Location.query.get_or_404(locationId)
    form = LocationForm()
    if form.validate_on_submit():
        location.locationName = form.locationName.data
        location.locationAddress = form.locationAddress.data
        db.session.commit()
        flash('Location Name has been updated.', 'success')
        return redirect(url_for("locations"))
    form.locationName.data = location.locationName
    form.locationAddress.data = location.locationAddress
    return render_template('addlocation.html', form=form, legend = 'Update Location')


# Product movement related routes
@app.route('/productmovement')
def productmovement():
    productmovements = ProductMovement.query.all()
    return render_template('productmovement.html', title="Product Movement", productmovements = productmovements)

@app.route('/addproductmovement', methods=['GET', 'POST'])
def addproductmovement():
    form = ProductMovementForm()
    # fetch all product and location data
    products = Product.query.all()
    locations = Location.query.all()
    # create list of products and choices for selectfield
    productsList = [(product.id, product.productName) for product in products]
    locationsList = [(None, 'Select Location')] + [(location.id, location.locationName) for location in locations]
    form.productName.default = None
    form.productName.choices = productsList
    form.fromLocation.choices = locationsList
    form.toLocation.choices = locationsList
    if form.validate_on_submit():
        productmovement = ProductMovement(date = str(form.date.data), fromLocationId = form.fromLocation.data, toLocationId = form.toLocation.data, productId = form.productName.data, productQuantity = form.productQuantity.data)
        db.session.add(productmovement)
        db.session.commit()
        flash('Product Movement has been added.', 'success')
        return redirect(url_for("productmovement"))
    return render_template('addproductmovement.html', title="Product Movements", form=form, legend = 'Add New Product Movement')


@app.route('/updateproductmovement/<int:productmovementId>', methods=['GET', 'POST'])
def updateproductmovement(productmovementId):
    productmovement = ProductMovement.query.get_or_404(productmovementId)
    form = ProductMovementForm()
    if form.validate_on_submit():
        productmovement.date = str(form.date.data)
        productmovement.fromLocationId = form.fromLocation.data
        productmovement.toLocationId = form.toLocation.data
        productmovement.productId = form.productName.data
        productmovement.productQuantity = form.productQuantity.data
        db.session.commit()
        flash('Product Movement has been updated.', 'success')
        return redirect(url_for("productmovement"))
    # fetch all product and location data
    products = Product.query.all()
    locations = Location.query.all()
    # create list of products and choices for selectfield
    productsList = [(product.id, product.productName) for product in products]
    locationsList = [(None, 'Select Location')] + [(location.id, location.locationName) for location in locations]
    form.productName.choices = productsList
    form.fromLocation.choices = locationsList
    form.toLocation.choices = locationsList
    form.date.data = productmovement.date
    if productmovement.fromLocationId:
        form.fromLocation.data = ""
    form.fromLocation.data = productmovement.fromLocationId
    form.toLocation.data = productmovement.toLocationId
    form.productName.data = productmovement.productId
    form.productQuantity.data = productmovement.productQuantity
    return render_template('addproductmovement.html', form=form, legend = 'Update Product Movement')


# Stock related routes
@app.route('/stock')
def stock():
    stock = Stock.query.all()
    return render_template('stock.html', title="Stock", stock = stock)



if __name__ == "__main__":
    app.run(debug=True)