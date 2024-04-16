from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.email = user_data["email"]
        self.password = user_data["password"]
        self.first_name = user_data["first_name"]

    @staticmethod
    def get(user_id):
        user_data = db.db.users.find_one({"_id": user_id})
        if user_data:
            return User(user_data)
        else:
            return None

    @staticmethod
    def create(email, password, first_name):
        user_data = {
            "email": email,
            "password": generate_password_hash(password, method='pbkdf2:sha256'),
            "first_name": first_name,
        }
        result = db.db.users.insert_one(user_data)
        return User.get(result.inserted_id)

    def check_password(self, password):
        return check_password_hash(self.password, password)


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data = db.db.users.find_one({"email": email})
        if user_data:
            user = User(user_data)
            if user.check_password(password):
                flash("Logged in", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email does not exist", category='error')
    return render_template("login.html", user=current_user)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = db.db.users.find_one({"email": email})
        if user:
            flash("Email already exists.", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = {
                "email": email,
                "first_name": first_name,
                "password": generate_password_hash(password1, method='pbkdf2:sha256')
            }
            db.db.users.insert_one(new_user)
            login_user(User(new_user), remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
