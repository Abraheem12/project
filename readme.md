# Chatty Bot
Chatty Bot is a conversational chatbot application designed using Flask and Jinja2. It offers a user-friendly chat interface allowing interactions with a bot, making it an engaging way to communicate with artificial intelligence.

## Student Information
- **Name:** Abraheem Zadron, Robin Shrestha, Carlos Garcia
- **Due Date:** May 01, 2024

## Overview
This application integrates user authentication, allowing users to have personalized experiences, and leverages the GPT-3 model from OpenAI for generating dynamic responses. It's structured with a clear separation of concerns, dividing the functionality into authentication handling, view management, and database modeling.

## Project Structure

The project is organized into several key components:
- `app.py`: The main entry point for the Flask application.
- `auth.py`: A Flask blueprint responsible for user authentication processes, including login, logout, and sign-up functionalities.
- `views.py`: Manages the application's views and integrates with the OpenAI GPT-3 model to facilitate chat interactions.
- `model.py`: Defines the database schema using SQLAlchemy, focusing on user management.
- `__init__.py`: Initializes the Flask application and ties together the various components.

### HTML Templates
- `base.html`: Serves as the foundation layout that other templates extend from.
- `login.html`: Template for the login page.
- `signup.html`: Template for the user sign-up page.
- `home.html`: The main chat interface where users interact with the bot.

## Features
- **User Authentication**: Secure sign-up and login functionality for user management.
- **Chat Interface**: A dynamic chat interface where users can send messages and receive responses from the bot.
- **GPT-3 Integration**: Leverages the powerful GPT-3 model for generating realistic and engaging responses.

## How to Run
1. Ensure you have Python and pip installed on your system.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Flask application:

```bash
flask run
```

## Dependencies
- Flask
- Jinja2
- Flask-Login
- SQLAlchemy
- OpenAI

## Styling
The application utilizes inline CSS within the `home.html` template for styling, providing a simple yet effective user interface design.


