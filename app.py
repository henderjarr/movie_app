"""flask and sqlalchemy app to manage movies and users"""
import os
from flask import Flask, redirect, render_template, request
from data_manager import DataManager
from models import db, Movie


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
    # Get all users from the database using the DataManager class
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Adds a new user to the database and returns back to the home page, POST"""
    # Get the user name from the form submission
    user_name = request.form.get('name')
    if user_name:
        data_manager.create_user(user_name)
    # Redirect back to the home page after adding the user
    return redirect('/')


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    """will return a list of all movies for a specific user, GET"""
    # Get all movies for the specified user from the database using the DataManager class
    user = data_manager.get_user(user_id)
    if not user:
        return render_template('404.html'), 404
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """will add a new movie for a specific user, POST"""
    title = request.form.get('title')
    movie_data = data_manager.fetch_movie_details(title)
    if not movie_data:
        return render_template('404.html'), 404

    new_movie = Movie(
        name=movie_data.get('Title'),
        director=movie_data.get('Director'),
        year=int(movie_data.get('Year')),
        poster_url=movie_data.get('Poster'),
        user_id=user_id
    )
    data_manager.add_movie(new_movie)
    return redirect(f'/users/{user_id}/movies')


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """will update a specific movie for a specific user, POST"""
    new_title = request.form.get('new_title')
    if new_title:
        data_manager.update_movie(movie_id, user_id, new_title)
    return redirect(f'/users/{user_id}/movies')


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """will delete a specific movie for a specific user, POST"""
    data_manager.delete_movie(user_id, movie_id)
    return redirect(f'/users/{user_id}/movies')


# error handling
@app.errorhandler(404)
def page_not_found(_):
    """Render a custom 404 error page"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(_):
    """Render a custom 500 error page"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)
