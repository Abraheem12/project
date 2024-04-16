from flask import Flask
from flask_pymongo import PyMongo
from os import getenv
from dotenv import load_dotenv
from flask_login import LoginManager

db = PyMongo()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv("SECRET_KEY")
    app.config['MONGO_URI'] = getenv("MONGO_URI")
    db.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    with app.app_context():
        from .auth import User
        db.db.users.create_index("email", unique=True)

    @login_manager.user_loader
    def load_user(id):
        from .auth import User
        user_data = db.db.users.find_one({"_id": id})
        return User(user_data) if user_data else None

    return app