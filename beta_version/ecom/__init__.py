from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
from flask_login import LoginManager
from flask_ngrok import run_with_ngrok
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import os

basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
#All the databases tables are stored in shop.db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
#Secret key is used for security purpose in case of cross site forging(Change key before use)
app.config['SECRET_KEY'] = 'hvewydbh643hvcjhv@#ycvdagc*874g'
#This are essentials for uploading images to the database (All images are uploaded to static/img folder)
app.config['UPLOADED_FILES_DEST']=os.path.join(basedir,'static/img')
photos = UploadSet('photos', IMAGES,default_dest=lambda x: 'ecom/static/img')
configure_uploads(app, photos)
patch_request_class(app)
#it initiates the SQLAlchemy 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
#bcrypt is used to hash the password stored for user
bcrypt = Bcrypt(app)
#This are essentials for login and logout purpose of user
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
#This files are imported at bottom to recover from circular import issue
from ecom import routes
#manager.run()
# run_with_ngrok(app)
