"""Seed the database with initial data"""

from models import db, User, Movie
from app import app

with app.app_context():

    db.create_all()  # Create tables if they don't exist

    user1 = User(name="Alice")
    user2 = User(name="Bob")
    user3 = User(name="Charlie")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    movie1 = Movie(name="Inception", director="Christopher Nolan", year=2010,
                   poster_url="https://example.com/inception.jpg", user_id=user1.id)
    movie2 = Movie(name="The Matrix", director="The Wachowskis", year=1999,
                   poster_url="https://example.com/matrix.jpg", user_id=user2.id)
    movie3 = Movie(name="Interstellar", director="Christopher Nolan", year=2014,
                   poster_url="https://example.com/interstellar.jpg", user_id=user1.id)
    movie4 = Movie(name="The Godfather", director="Francis Ford Coppola", year=1972,
                   poster_url="https://example.com/godfather.jpg", user_id=user3.id)
    movie5 = Movie(name="Pulp Fiction", director="Quentin Tarantino", year=1994,
                   poster_url="https://example.com/pulpfiction.jpg", user_id=user2.id)

    db.session.add_all([movie1, movie2, movie3, movie4, movie5])
    db.session.commit()
