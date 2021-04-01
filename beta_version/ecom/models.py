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
    profile = db.Column(db.String(180), unique=False,
                        nullable=False, default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username

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
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))
    image1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image3 = db.Column(db.String(150), nullable=False, default='image3.jpg')

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

# class Type(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     Type = db.Column(db.String(45), nullable=False)

# class Status(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     Status = db.Column(db.String(45), nullable=False )

# class State(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     State = db.Column(db.String(45), nullable=False)

# class SubState(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     SubState = db.Column(db.String(45), nullable=False)
#     State_ID = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
#     State = db.relationship('state', backref=db.backref('State_details', lazy=True))

# class Delivery(db.Model):
#     Delivery_ID = db.Column(db.String(8), primary_key=True, nullable=False)
#     Delivery_Reg_Time = db.Column(db.DateTime,auto_now_add=True, nullable=False)
#     Delivery_Est_Date = db.Column(db.Date, nullable=False)
#     Delivery_Sender = db.Column(db.String(45), nullable=False)
#     Delivery_Sender_Phone = db.Column(db.String(8), nullable=False)
#     State_ID = db.column(db.Integer, db.ForeignKey('state.id'))
#     State = db.relationship('state', backref=db.backref('State', lazy=True))
#     SubState_ID = db.column(db.Integer, db.ForeignKey('SubState.id'))
#     SubState = db.relationship('sub_state', backref=db.backref('SubState', lazy=True))
#     From_Address = db.Column(db.String(255), nullable=False)
#     Delivery_Recipient = db.Column(db.String(45), nullable=False)
#     Delivery_Recipient_Phone = db.Column(db.String(8), nullable=False)
#     To_State_ID = db.column(db.Integer, db.ForeignKey('To_State.id'))
#     To_State = db.relationship('state', backref=db.backref('State', lazy=True))
#     To_SubState_ID = db.column(db.Integer, db.ForeignKey('To_SubState.id'))
#     To_SubState = db.relationship('sub_state', backref=db.backref('SubState', lazy=True))
#     To_Address = db.Column(db.String(255), nullable=False)
#     Delivery_Total = db.Column(db.Float, nullable=False)
#     Status_ID = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
#     Status = db.relationship('status', backref=db.backref('status', lazy=True))
#     Status_Reason = db.Column(db.String(255), nullable=True)
#     # User = db.Column.ForeignKey(User, editable=True, blank=True, nullable=True, limit_choices_to={'groups__name': u"Хэрэглэгч"})
#     User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     User = db.relationship('user', backref= db.backref('User', lazy=True))

#     def __str__(self):
#         return self.Delivery_ID

#     def save(self, *args, **kwargs):
#         if self.Delivery_ID:
#             super(Delivery, self).save(*args, **kwargs)
#             return

#         unique = False
#         while not unique:
#             try:
#                 letters = string.ascii_letters
#                 self.Delivery_ID = ''.join(random.choice(letters) for i in range(8))
#                 super(Delivery, self).save(*args, **kwargs)
#             except IntegrityError:
#                 letters = string.ascii_letters
#                 self.Delivery_ID = ''.join(random.choice(letters) for i in range(8))
#             else:
#                 unique = True

# class Shipment(db.Model):
    
#     Shipment_ID = db.Column(db.Integer, primary_key=True, nullable=False)
#     Shipment_Weight = db.Column(db.Float, nullable=False)
#     Type_ID = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
#     Type = db.relationship('type', backref=db.backref('Type', lazy=True))
#     Shipment_Note = db.Column(db.Text(500))
#     Delivery_ID = db.Column(db.String(8), db.ForeignKey('delivery.Delivery_ID'))
#     Delivery = db.relationship('delivery', backref=db.backref('Delivery', lazy=True))


db.create_all()