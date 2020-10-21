from __main__ import db

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    productName = db.Column(db.String(100), unique = True, nullable = False)

# Location Model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    locationName = db.Column(db.String(100), nullable = False)
    locationAddress = db.Column(db.String(200), nullable = False)


db.create_all()