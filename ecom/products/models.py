from ecom import db
from datetime import datetime

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


db.create_all()
