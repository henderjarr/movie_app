"""handle the database operations for the User and Movie models"""
from models import db, User, Movie


class DataManager():
    """handles the database operations for the User and Movie models"""
    # User operations

    def get_users(self):
        """get all users from the database"""
        return db.session.scalars(db.select(User)).all()

    def create_user(self, name):
        """Create a new user in the database"""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    # Movie operations
    def get_movies(self, user_id):
        """get all movies for a specific user from the database"""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Add a new movie to the database"""
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """Update the title of a movie in the database"""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
            return True
        return False

    def delete_movie(self, movie_id):
        """Delete a movie from the database"""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False
