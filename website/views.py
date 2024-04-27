# Importing necessary modules from flask
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
# Importing necessary functions from flask_login
from flask_login import login_required, current_user
# Importing openai for interacting with the GPT-3 model
import openai
# Importing os for environment variable management
import os
# Importing dotenv for loading environment variables from a .env file
from dotenv import load_dotenv

# Loading the environment variables from the .env file
load_dotenv()

# Creating a Blueprint named 'views'
views = Blueprint('views', __name__)

# Setting the API key for openai
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to chat with the GPT-3 model


def chatWithGPT(prompt):
    # Creating a chat completion with the GPT-3 model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    # Returning the content of the first choice
    return response.choices[0].message.content.strip()

# Route for the home page


@views.route('/', methods=['GET', 'POST'])
@login_required  # User must be logged in to access this route
def home():
    # If the request method is POST
    if request.method == 'POST':
        # Get the user's input from the form
        user_input = request.form['user_input']
        # Get the response from the GPT-3 model
        response = chatWithGPT(user_input)
        # If the chat history is not in the session, create it
        if 'chat_history' not in session:
            session['chat_history'] = []
        # Append the user's input and the bot's response to the chat history
        session['chat_history'].append({'user': user_input, 'bot': response})
        # Tell Flask to save the session data
        session.modified = True
        # Redirect to the same page
        return redirect(url_for('views.home'))

    # Get the user's first name if they are logged in, otherwise use "User"
    user_name = current_user.first_name if current_user else "User"
    # Get the chat history from the session, or create a new one if it doesn't exist
    chat_history = session.get('chat_history', [{'user': user_name, 'bot': f'Hello {
                               user_name}, how can I help you today?'}])
    # Render the home page
    return render_template("home.html", user=current_user, chat_history=chat_history)
