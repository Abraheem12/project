# Importing necessary modules from flask
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
# Importing User model
from .models import User
# Importing password hashing and checking functions
from werkzeug.security import generate_password_hash, check_password_hash
# Importing database instance from __init__.py
from . import db
# Importing necessary functions from flask_login
from flask_login import login_user, login_required, logout_user, current_user

# Creating a Blueprint named 'auth'
auth = Blueprint('auth', __name__)

# Route for login page


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If the request method is POST
    if request.method == 'POST':
        # Get email and password from the form
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the database for the user with the given email
        user = User.query.filter_by(email=email).first()
        # If the user exists
        if user:
            # If the password is correct
            if check_password_hash(user.password, password):
                # Flash a success message
                flash("Logged in", category='success')
                # Log the user in
                login_user(user, remember=True)
                # Clear the chat history
                session.pop('chat_history', None)
                # Redirect to the home page
                return redirect(url_for('views.home'))
            else:
                # If the password is incorrect, flash an error message
                flash("Incorrect", category='error')
        else:
            # If the user does not exist, flash an error message
            flash("Email does not exist", category='error')
    # Render the login page
    return render_template("login.html", user=current_user)

# Route for logout


@auth.route('logout')
@login_required  # User must be logged in to access this route
def logout():
    # Log the user out
    logout_user()
    # Clear the chat history
    session.pop('chat_history', None)
    # Redirect to the login page
    return redirect(url_for('auth.login'))

# Route for sign-up page


@auth.route('sign-up', methods=['GET', 'POST'])
def sign_up():
    # If the request method is POST
    if request.method == 'POST':
        # Get the form data
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Query the database for the user with the given email
        user = User.query.filter_by(email=email).first()
        # If the user exists, flash an error message
        if user:
            flash("Email already exists.", category='error')
        # If the email is too short, flash an error message
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        # If the first name is too short, flash an error message
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        # If the passwords do not match, flash an error message
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        # If the password is too short, flash an error message
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # If all the data is valid, create a new user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            # Log the new user in
            login_user(new_user, remember=True)
            # Flash a success message
            flash('Account created!', category='success')
            # Redirect to the home page
            return redirect(url_for('views.home'))

    # Render the sign-up page
    return render_template("sign_up.html", user=current_user)
