from . import db # this works because were in the same directory where the database was made if we were outside we would do something like from website import db
from flask_login import UserMixin #Flask login is just a module that helps us log users in 
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
