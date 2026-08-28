"""flask and sqlalchemy app to manage movies and users"""
import os
from flask import Flask, render_template
from data_manager import DataManager
from models import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link the database and the app. This is the reason you need to import db from models
db.init_app(app)

data_manager = DataManager()  # Create an object of your DataManager class


@app.route('/')
def home():
    """show a list of all registered users and a form for adding new users, GET"""
    return render_template('home.html')


@app.route('/users', methods=['POST'])
def list_users():
    """Adds a new user to the database and returns back to the home page, POST"""
    users = data_manager.get_users()
    # Debugging: print users to the console
    print([user.name for user in users])
    # need to unpack the users list to pass it to the template
    # Temporarily returning user names as a string
    return str([user.name for user in users])
    # return str(users)  # Temporarily returning users as a string


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    """will return a list of all movies for a specific user, GET"""


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """will add a new movie for a specific user, POST"""
    # good place to use the omdB API to get movie details based on the title provided in the request


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """will delete a specific movie for a specific user, PUT"""


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)
