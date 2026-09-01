"""handle the database operations for the User and Movie models"""
import os
import requests
from dotenv import load_dotenv
from models import db, User, Movie

load_dotenv()

IMDB_API_KEY = os.getenv('IMDB_API_KEY')
IMDB_BASE_URL = os.getenv('IMDB_BASE_URL')


class DataManager():
    """handles the database operations for the User and Movie models"""
    # User operations

    def get_users(self):
        """get all users from the database"""
        return db.session.scalars(db.select(User)).all()

    def get_user(self, user_id):
        """get a specific user from the database"""
        return db.session.scalars(db.select(User).where(User.id == user_id)).first()

    def create_user(self, name):
        """Create a new user in the database"""
        new_user = User(name=name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    # Movie operations
    def get_movies(self, user_id):
        """get all movies for a specific user from the database"""
        return db.session.scalars(db.select(Movie).where(Movie.user_id == user_id)).all()

    def add_movie(self, movie):
        """Add a new movie to the database"""
        db.session.add(movie)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def update_movie(self, movie_id, user_id, new_title):
        """Update the title of a movie in the database"""
        movie = db.session.scalars(db.select(Movie).where(
            Movie.id == movie_id, Movie.user_id == user_id)).first()
        if movie:
            movie.name = new_title
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            return True
        return False

    def delete_movie(self, user_id, movie_id):
        """Delete a movie from the database where it matches the user_id and movie_id"""
        movie = db.session.scalars(db.select(Movie).where(
            Movie.id == movie_id, Movie.user_id == user_id)).first()
        if movie:
            db.session.delete(movie)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            return True
        return False

    # IMDB API operations
    def fetch_movie_details(self, title):
        """Fetch movie details from the IMDB API"""
        params = {
            't': title,  # t = format for title search, i = identifier search if you have the IMDB ID
            'apikey': IMDB_API_KEY
        }
        try:
            # add timeout to avoid hanging requests
            response = requests.get(IMDB_BASE_URL, params=params, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie details: {e}")
            return None
