#This will import the flask app from __init__.py of ecom folder.
from ecom import app
if __name__ == '__main__':
	#You can set debug=True to start debugging 
    app.run()
