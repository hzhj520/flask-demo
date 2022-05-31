from flask import Flask
from flask_jwt_extended import JWTManager

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import views, views2

# Load the config file
app.config.from_object('config')

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']