from flask import Blueprint, render_template, request, flash, session, redirect, url_for
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
@login_required
def home():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = chatWithGPT(user_input)
        session['response'] = response
        return redirect(url_for('views.home'))  # Redirect to the same page

    user_name = current_user.first_name if current_user else "User"
    response = session.pop('response', f'Hello {user_name}, how can I help you today?')
    return render_template("home.html", user=current_user, response=response)



