# Importing the create_app function from the website package
from website import create_app

# Creating a Flask application by calling the create_app function
app = create_app()

# Checking if this script is the main entry point of the program
if __name__ == '__main__':
    # Running the Flask application in debug mode on port 5001
    app.run(debug=True, port=5001)
