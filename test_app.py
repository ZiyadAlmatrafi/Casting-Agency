import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import *
from models import *


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://postgres:123@localhost:5432/capstone_test'
        setup_db(self.app, self.database_path)
        
        self.new_movie = {
            "title":"The movie",
            "release":"2/2/2022"
        }
        self.update_movie = {
            "title":"The movie 111"
        }
        self.new_actor = {
            "name":"Ziyad",
            "age":"24",
            "gender":"Male"
        }
        self.update_actor = {
            "name":"New Ziyad 111"
        }

        self.casting_assistant="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFHc3J4Ul9fRW4xRDFiZ2pibWF5RCJ9.eyJpc3MiOiJodHRwczovL3ppeWFkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGU2YWRiYjVhNmYzZjAwNjg3YWJjZjQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYzMDY5ODI1OCwiZXhwIjoxNjMwNzg0NjU4LCJhenAiOiJhTGVueTU5dFNGcTdlejJFQWhXbEs2QThoTHpGMVJaSiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.1QgRdL_HiPJ6tbadBeFI4-gq-8FCfJR4thxTMbuPKu4sZnGCYKXDGp7KOM0LmC2XfiJXMW70urQTO69_A_UnFZqp5H2ihlQuz0Z4HJ54XEqJYkuOQpW7I5wFd1uRSIrTGCrY7xBMfVQ9qaqgYtOnXWkvcKr_3Tk3v4RpjaQ9Ezrkz6NaMepWNy372QNq6-heNH4DNxuO6T6oOnTXHqVkGFhkxAiCI4Tx654boJjnkeK1qVlYJ-SdLz7uASK0wsgrl8eqPamM-gDH7hs406_W4wqDCTo9olYVYfkmMg6iUzSf3pnlEDRSn8XVDZms1gsYIiYDqlogHzUUuLg7-tf7RQ"
        self.casting_director="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFHc3J4Ul9fRW4xRDFiZ2pibWF5RCJ9.eyJpc3MiOiJodHRwczovL3ppeWFkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGZlN2RiMThhMWMwNjAwNjg5N2FjNGQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYzMDY5ODEyNywiZXhwIjoxNjMwNzg0NTI3LCJhenAiOiJhTGVueTU5dFNGcTdlejJFQWhXbEs2QThoTHpGMVJaSiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.CQ_yjdlEXccS0qsYZx3et6OdlKoz3sQv5_tV8VKPVD0wXqOFXYjTLF-eMhHhVphEOkDx1d2RPNYe8YyMFULJn3PRHP1M_3oiPeeR4VDHSt5CCsLa7STyLkmGiRDslNA6OfSux-hICPDXTHATuH6eAa3V2B4lw5COxtfkOBJZs7WKO25wxuj_SPPDVpKyGc_932lOjNuf9DnAwGkE6uGAn9lcgsjcRQ0muVDEqXLhVhrh3LMQieEUWs3ezlubymCK5GhoNF-drM8FaJGS0pGx2D68t0EQEbdANUobTIdFXMGcy7YAD5-lZIArzaHk_KlLUCxvxZB6AltI8K0bdmugig"
        self.executive_producer="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFHc3J4Ul9fRW4xRDFiZ2pibWF5RCJ9.eyJpc3MiOiJodHRwczovL3ppeWFkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGZlN2VlM2Y0NjJiMjAwNzFiYTA1MjQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYzMDY5Nzk3NiwiZXhwIjoxNjMwNzg0Mzc2LCJhenAiOiJhTGVueTU5dFNGcTdlejJFQWhXbEs2QThoTHpGMVJaSiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.zuY2OWXEjvksKGF0MFCIBk1otQvBAOIjGpJiggVTGKeWsnZPI0fUA1Fx0bbtnKRAdMojtS5QKJ1xYOlQZt8jDZEehx217IupZTmd6JcVZZ7gfcoDw-dokVDsYZdOmV8SJd1kI9rAC0DoNQVKXH-G1qlSjLwokau-r0a8kF7TsqZ5asmCWv2Lh75WKIq558oPp-_iaVWzNyOtHdAXh75tpf927mnqzyTWfVBGPKtLbwNzN-ua7X88XwK6ZXUjoiI0hm012SlKr7Df9L3XlX7TuOPUdpzQ9PCQ6K6dHxRhWrvMCQ1x7ZdGwgQbT9G2-v65AuH_q600a4TPCP_VvSnjJw"

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        # self.db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # get movies test
    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": 'bearer ' + self.casting_assistant})
        self.assertEqual(res.status_code, 200)

    def test_get_movies_not_found(self):
        res = self.client().get('/movies/', headers={"Authorization": 'bearer ' + self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # get actors test
    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": 'bearer ' + self.casting_assistant})
        self.assertEqual(res.status_code, 200)

    def test_actors_not_allowed(self):
        res = self.client().get('/actors/1', headers={"Authorization": 'bearer ' + self.casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    #  Delete a movie test   //remove comment to test it//
    # def test_delete_movie(self):
        # res = self.client().delete('/movies/3', headers={"Authorization": 'bearer ' + self.executive_producer})

        # movie = Movie.query.filter(Movie.id == 3).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(movie, None)

    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/330', headers={"Authorization": 'bearer ' + self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie_not_authorized(self):
        res = self.client().delete('/movies/330')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Delete an actor test  //remove comment to test it//
    # def test_delete_actor(self):
    #     res = self.client().delete('/actors/3', headers={"Authorization": 'bearer ' + self.casting_director})

        # actor = Actor.query.filter(Actor.id == 3).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(movie, None)

    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/330', headers={"Authorization": 'bearer ' + self.casting_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # POST a new movie test
    # def test_create_new_movie(self):
    #     res = self.client().post('/add-movie', json=self.new_movie, headers={"Authorization": 'bearer ' + self.executive_producer})
    #     self.assertEqual(res.status_code, 200)

    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": 'bearer ' + self.executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    # POST a new actor test
    def test_create_new_actor(self):
        res = self.client().post('/add-actor', json=self.new_actor, headers={"Authorization": 'bearer ' + self.casting_director})
        self.assertEqual(res.status_code, 200)

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    # Update a movie
    def test_update_movie(self):
        res = self.client().patch('/movies/1', json=self.update_movie, headers={"Authorization": 'bearer ' + self.executive_producer})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
    
    def test_update_movie_not_found(self):
        res = self.client().patch('/movies/100', json=self.update_movie, headers={"Authorization": 'bearer ' + self.executive_producer})
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Update an actor
    def test_update_actor(self):
        res = self.client().patch('/actors/1', json=self.update_actor, headers={"Authorization": 'bearer ' + self.executive_producer})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    def test_update_actor_not_found(self):
        res = self.client().patch('/actors/100', json=self.update_movie, headers={"Authorization": 'bearer ' + self.executive_producer})
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()