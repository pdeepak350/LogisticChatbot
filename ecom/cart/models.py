from ecom import db,login_manager
from flask_login import UserMixin
from ecom.products.models import Addproduct

@login_manager.user_loader
def load_cart(user_id):
    return Cart.query.get(int(user_id))

class Cart(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Addproduct",  on_delete=models.CASCADE))
    name = db.Column(db.String(80), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False,
                        nullable=False, default='profile.jpg')

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()
#product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image1, 'colors':product.color