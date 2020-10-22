from __main__ import db
import random

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    productName = db.Column(db.String(100), unique = True, nullable = False)

    def __repr__(self):
        return self.productName

# Location Model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    locationName = db.Column(db.String(100), nullable = False)
    locationAddress = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return self.locationName

# Product Movement Model
class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(15), nullable = False)
    fromLocationId = db.Column(db.Integer, db.ForeignKey(Location.id))
    toLocationId = db.Column(db.Integer, db.ForeignKey(Location.id))
    productId = db.Column(db.Integer, db.ForeignKey(Product.id))
    fromLocation = db.relationship(Location, foreign_keys=[fromLocationId])
    toLocation = db.relationship(Location, foreign_keys=[toLocationId])
    productName = db.relationship(Product, foreign_keys=[productId])
    productQuantity = db.Column(db.Integer, db.CheckConstraint(
        'productQuantity > 0'))
    
    def __repr__(self):
        return f'{self.date}\t{self.fromLocation}\t{self.toLocation}\t{self.productName}\t{self.productQuantity}'
    
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    locationId = db.Column(db.Integer, db.ForeignKey(Location.id))
    productId = db.Column(db.Integer, db.ForeignKey(Product.id))
    locationName = db.relationship(Location, foreign_keys=[locationId])
    productName = db.relationship(Product, foreign_keys=[productId])
    availableStock = db.Column(db.Integer, db.CheckConstraint(
        'availableStock > 0'))


db.create_all()