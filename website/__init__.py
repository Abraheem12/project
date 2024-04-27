# Importing necessary modules from flask
from flask import Flask
# Importing SQLAlchemy for database management
from flask_sqlalchemy import SQLAlchemy
# Importing path from os for file path management
from os import path
# Importing LoginManager from flask_login for user session management
from flask_login import LoginManager
# Importing getenv from os for environment variable management
from os import getenv

# Creating a SQLAlchemy object
db = SQLAlchemy()
# Setting the database name
DB_NAME = "database.db"

# Function to create the Flask app


def create_app():
    # Creating a Flask app
    app = Flask(__name__)
    # Setting the secret key from an environment variable, or using a default value
    app.config['SECRET_KEY'] = getenv('SECRET_KEY', 'default_secret_key')
    # Setting the database URI from an environment variable, or using a default value
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    # Initializing the database with the app
    db.init_app(app)

    # Importing the views and auth blueprints
    from .views import views
    from .auth import auth

    # Registering the blueprints with the app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Importing the User model. This is done here so that the model is defined before the database is created
    from .models import User

    # Creating all the database tables
    with app.app_context():
        db.create_all()

    # Creating a LoginManager object
    login_manager = LoginManager()
    # Setting the view to redirect to when the user needs to log in
    login_manager.login_view = 'auth.login'
    # Initializing the login manager with the app
    login_manager.init_app(app)

    # Defining the user loader function. This function tells flask_login how to find a specific user from their ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    # Returning the created app
    return app

# Function to create the database if it doesn't exist


def create_database(app):
    # If the database file doesn't exist
    if not path.exists('website/' + DB_NAME):
        # Create all the database tables
        db.create_all(app=app)
        # Print a message indicating that the database was created
        print('Created Database!')
