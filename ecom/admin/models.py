from ecom import db,login_manager
from flask_login import UserMixin

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


db.create_all()
