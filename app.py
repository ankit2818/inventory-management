from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from forms import ProductForm, LocationForm, ProductMovementForm
from config import Config
import random


app = Flask(__name__)
app.config.from_object(Config)

# Database
db = SQLAlchemy(app)

# Import Models
from models import Product, Location, ProductMovement

# Choose Random Username
def username():
    usernameList = ["Hermione Granger", "Harry Potter", "Ron Weasley"]
    return random.choice(usernameList)

# utils
def getQuantity(location, product):
    incoming = ProductMovement.query.filter(ProductMovement.toLocationId == location, ProductMovement.productId == product).from_self(func.sum(ProductMovement.productQuantity, )).all()
    outgoing = ProductMovement.query.filter(ProductMovement.fromLocationId == location, ProductMovement.productId == product).from_self(func.sum(ProductMovement.productQuantity, )).all()
    if incoming[0][0] == None:
        incoming = 0
    else:
        incoming = incoming[0][0]
    if outgoing[0][0] == None:
        outgoing = 0
    else:
        outgoing = outgoing[0][0]
    available = incoming - outgoing
    return available if available >= 0 else 0

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
    if form.validate_on_submit() or request.method == 'POST':
        product = Product(productName = form.productName.data)
        try:
            db.session.add(product)
            db.session.commit()
            flash('Product has been added.', 'success')
            return redirect(url_for("products"))
        except:
            flash('Database Error.', 'danger')
            return redirect(url_for("products"))
    return render_template('addproduct.html', title="Products", form=form, legend = 'Add New product')

@app.route('/updateproduct/<int:productId>', methods=['GET', 'POST'])
def updateproduct(productId):
    product = Product.query.get_or_404(productId)
    form = ProductForm()
    if form.validate_on_submit() or request.method == 'POST':
        product.productName = form.productName.data
        try:
            db.session.commit()
            flash('Product Name has been updated.', 'success')
            return redirect(url_for("products"))
        except:
            flash('Database Error.', 'danger')
            return redirect(url_for("products"))
    form.productName.data = product.productName
    return render_template('addproduct.html', form = form, legend = 'Update Product')


# Location related routes
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', title="Locations", locations=locations)

@app.route('/addlocation', methods=['GET', 'POST'])
def addlocation():
    form = LocationForm()
    if form.validate_on_submit() or request.method == 'POST':
        location = Location(locationName = form.locationName.data, locationAddress = form.locationAddress.data)
        try:
            db.session.add(location)
            db.session.commit()
            flash('Location has been added.', 'success')
            return redirect(url_for("locations"))
        except:
            flash('Database Error.', 'danger')
            return redirect(url_for("locations"))
    return render_template('addlocation.html', title="Locations", form=form, legend = 'Add New location')

@app.route('/updatelocation/<int:locationId>', methods=['GET', 'POST'])
def updatelocation(locationId):
    location = Location.query.get_or_404(locationId)
    form = LocationForm()
    if form.validate_on_submit() or request.method == 'POST':
        location.locationName = form.locationName.data
        location.locationAddress = form.locationAddress.data
        try:
            db.session.commit()
            flash('Location Name has been updated.', 'success')
            return redirect(url_for("locations"))
        except:
            flash('Database Error.', 'danger')
            return redirect(url_for("locations"))
    form.locationName.data = location.locationName
    form.locationAddress.data = location.locationAddress
    return render_template('addlocation.html', form = form, legend = 'Update Location')


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
    if form.validate_on_submit() or request.method == 'POST':
        date = str(form.date.data)
        fromLocationId = form.fromLocation.data
        toLocationId = form.toLocation.data
        productId = form.productName.data
        productQuantity = form.productQuantity.data
        # From location is none
        if fromLocationId == "None":
            try:
                productmovement = ProductMovement(date = date, fromLocationId = fromLocationId, toLocationId = toLocationId, productId = productId, productQuantity = productQuantity)
                db.session.add(productmovement)
                db.session.commit()
                flash('Product Movement has been added.', 'success')
                return redirect(url_for("productmovement"))
            except:
                flash('Database Error.', 'danger')
                return redirect(url_for("productmovement"))
        elif fromLocationId == toLocationId:
            flash('Cannot move to same location.', 'warning')
        else:
            presentQuantity = getQuantity(fromLocationId, productId)
            if presentQuantity < int(form.productQuantity.data):
                flash(f'Not enough quantity available. Max available: {presentQuantity}', 'warning')
            else:
                try:
                    productmovement = ProductMovement(date = date, fromLocationId = fromLocationId, toLocationId = toLocationId, productId = productId, productQuantity = productQuantity)
                    db.session.add(productmovement)
                    db.session.commit()
                    flash('Product Movement has been added.', 'success')
                    return redirect(url_for("productmovement"))
                except:
                    flash('Database Error.', 'danger')
                    return redirect(url_for("productmovement"))
    return render_template('addproductmovement.html', title="Product Movements", form = form, legend = 'Add New Product Movement')


@app.route('/updateproductmovement/<int:productmovementId>', methods=['GET', 'POST'])
def updateproductmovement(productmovementId):
    productmovement = ProductMovement.query.get_or_404(productmovementId)
    form = ProductMovementForm()
    if form.validate_on_submit() or request.method == 'POST':
        productmovement.date = str(form.date.data)
        productmovement.fromLocationId = form.fromLocation.data
        productmovement.toLocationId = form.toLocation.data
        productmovement.productId = form.productName.data
        productmovement.productQuantity = form.productQuantity.data
        print("Test")
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
    form.date.default = productmovement.date
    form.fromLocation.default = productmovement.fromLocationId
    form.toLocation.default = productmovement.toLocationId
    form.productName.default = productmovement.productId
    form.productQuantity.default = productmovement.productQuantity
    form.process()
    return render_template('addproductmovement.html', form=form, legend = 'Update Product Movement')


# Stock related routes
@app.route('/stock')
def stock():
    try:
        locations = Location.query.all()
        products = Product.query.all()
        stockAvailable = []
        for location in locations:
            for product in products:
                temp = {}
                temp['locationName'] = location.locationName
                temp['productName'] = product.productName
                temp['availableQuantity'] = getQuantity(location.id, product.id)
                stockAvailable.append(temp)
        return render_template("stock.html", stockAvailable = stockAvailable)
    except:
        return render_template("stock.html", stockAvailable = {})

if __name__ == "__main__":
    app.run(debug=True)