"""Seed the database with initial data"""
from models import db, User, Movie
from data_manager import DataManager
from app import app


data_manager = DataManager()

with app.app_context():

    user1 = User(name="Alice")
    user2 = User(name="Bob")
    user3 = User(name="Charlie")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    inception = data_manager.fetch_movie_details("Inception")
    matrix = data_manager.fetch_movie_details("The Matrix")
    interstellar = data_manager.fetch_movie_details("Interstellar")
    godfather = data_manager.fetch_movie_details("The Godfather")
    pulpfiction = data_manager.fetch_movie_details("Pulp Fiction")

    movie1 = Movie(name=inception.get("Title"), director=inception.get("Director"),
                   year=int(inception.get("Year", 0)), poster_url=inception.get("Poster"),
                   user_id=user1.id)
    movie2 = Movie(name=matrix.get("Title"), director=matrix.get("Director"),
                   year=int(matrix.get("Year", 0)), poster_url=matrix.get("Poster"),
                   user_id=user2.id)
    movie3 = Movie(name=interstellar.get("Title"), director=interstellar.get("Director"),
                   year=int(interstellar.get("Year", 0)), poster_url=interstellar.get("Poster"),
                   user_id=user1.id)
    movie4 = Movie(name=godfather.get("Title"), director=godfather.get("Director"),
                   year=int(godfather.get("Year", 0)), poster_url=godfather.get("Poster"),
                   user_id=user3.id)
    movie5 = Movie(name=pulpfiction.get("Title"), director=pulpfiction.get("Director"),
                   year=int(pulpfiction.get("Year", 0)), poster_url=pulpfiction.get("Poster"),
                   user_id=user2.id)

    db.session.add_all([movie1, movie2, movie3, movie4, movie5])
    db.session.commit()
