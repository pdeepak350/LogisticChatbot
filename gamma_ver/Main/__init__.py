from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

app.config['SECRET_KEY'] = 'hvewydbh643hvcjhv@#ycvdagc*874g'

app.config['UPLOADED_FILES_DEST']=os.path.join(basedir,'static/img')
photos = UploadSet('photos', IMAGES,default_dest=lambda x: 'Main/static/img')
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from Main import routes
# manager.run()