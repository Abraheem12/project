from flask import Blueprint, render_template, request 
from flask_login import login_required, current_user
import openai
import os
from dotenv import load_dotenv
load_dotenv()

views = Blueprint('views', __name__)

openai.api_key = os.getenv('OPENAI_API_KEY')


def chatWithGPT(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


@views.route('/', methods=['GET', 'POST'])
def home():
    user_input = None
    response = None
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        # Process the user_input with your chatbot here...
        response = chatWithGPT(user_input)
    return render_template('home.html', user=current_user, user_input=user_input, response=response)
