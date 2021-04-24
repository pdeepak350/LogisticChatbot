from ecom import db,login_manager
from flask_login import UserMixin
from flask_sqlalchemy import model
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import random
import string

#Used for login and logout purpose of the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Database table User to store user information in the database
# nullable means the form field cant be empty
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)

class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)

# Addproduct table to store the information about the products
# All fields are required 
# brand_id and category_id are foreign keys that are referenced to Brand and Category table
# That is In case you want to delete any brand or category from database you need to first delete 
# the products which contains that brand or category otherwise the database gets affected
class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    color = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))
    image1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image3 = db.Column(db.String(150), nullable=False, default='image3.jpg')
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=False)
    merchant = db.relationship('Merchant', backref=db.backref('merchant', lazy=True))
    merchant_name = db.Column(db.String(45), nullable=False)
    merchant_phone = db.Column(db.Integer, nullable=False)
    merchant_address = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Addproduct %r>' % self.name

# Brand table contains name and id of brand
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

# Category table contains name and id of category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    User = db.relationship(User, backref=db.backref('users', lazy=True))
    product_id = db.Column(db.Integer, db.ForeignKey('addproduct.id'), nullable=False)
    Addproduct = db.relationship(Addproduct, backref=db.backref('products', lazy=True))
    color = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Delivery(db.Model):
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('addproduct.id'), nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=False)
    color = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    Delivery_ID = db.Column(db.String(8), primary_key=True, nullable=False)
    Delivery_Reg_Time = db.Column(db.DateTime,auto_now_add=True, nullable=False)
    Delivery_Est_Date = db.Column(db.Date, nullable=False)
    Delivery_Sender = db.Column(db.String(45), db.ForeignKey('addproduct.merchant_name'), nullable=False)
    Delivery_Sender_Phone = db.Column(db.String(8), db.ForeignKey('addproduct.merchant_phone'), nullable=False)
    From_Address = db.Column(db.String(255), db.ForeignKey('addproduct.merchant_address'), nullable=False)
    Delivery_Recipient = db.Column(db.String(45), nullable=False)
    Delivery_Recipient_Phone = db.Column(db.String(8), nullable=False)
    To_Address = db.Column(db.String(255), nullable=False)
    Status_Reason = db.Column(db.String(255), nullable=True)

class Shipment(db.Model):   
    Shipment_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Shipment_Note = db.Column(db.Text(500))
    Delivery_ID = db.Column(db.String(8), db.ForeignKey('delivery.Delivery_ID'))

db.create_all()