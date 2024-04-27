# Importing the database instance from the current package. This works because we're in the same directory where the database was created. If we were outside, we would do something like from website import db
from . import db

# Importing UserMixin from flask_login. Flask login is a module that helps us manage user sessions
from flask_login import UserMixin

# Importing func from sqlalchemy.sql for SQL functions
from sqlalchemy.sql import func

# Defining the User model. It inherits from db.Model and UserMixin


class User(db.Model, UserMixin):
    # Defining the id column. It is an integer and is the primary key
    id = db.Column(db.Integer, primary_key=True)

    # Defining the email column. It is a string of maximum 100 characters and must be unique
    email = db.Column(db.String(100), unique=True)

    # Defining the password column. It is a string of maximum 100 characters
    password = db.Column(db.String(100))

    # Defining the first_name column. It is a string of maximum 100 characters
    first_name = db.Column(db.String(100))
