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

        self.casting_assistant="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFHc3J4Ul9fRW4xRDFiZ2pibWF5RCJ9.eyJpc3MiOiJodHRwczovL3ppeWFkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGU2YWRiYjVhNmYzZjAwNjg3YWJjZjQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYzMDc4MTE5MiwiZXhwIjoxNjMwODY3NTkyLCJhenAiOiJhTGVueTU5dFNGcTdlejJFQWhXbEs2QThoTHpGMVJaSiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.xOPRWSErG0wyiOX1vCyDysoVXmmbjKCI6aBtjiL_Yxa0M4M9Q6ZJ2nAXPdB4el3xE7kRpspNo-9zwlhgzvEYMG4y14wBqQEIX0gwA7Zmwmk_zLRKUVe_Rlsq8_e-qH_5eBbPvL6N5ZDOZJPz850Dio5wYQHYmL7KttO6xk9KRGfZygbwFEEz2YfxmfHaJNR2M9C1rb4toKrG1MQ9h8T0dYC99UmJDnkWSWbA3Tne79ixhPdhFcPWDiuplX9IE7sTV16wH5hnjEXLAyzwSEDz3GYRculgDHDmWFUhgEDbFlbJeL5PXkN-P47yAfblsSuWu-JTPpzBCkynFUtEE0Tdqg"
        self.casting_director="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFHc3J4Ul9fRW4xRDFiZ2pibWF5RCJ9.eyJpc3MiOiJodHRwczovL3ppeWFkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGZlN2RiMThhMWMwNjAwNjg5N2FjNGQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYzMDc4MTQ0NCwiZXhwIjoxNjMwODY3ODQ0LCJhenAiOiJhTGVueTU5dFNGcTdlejJFQWhXbEs2QThoTHpGMVJaSiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.XIxkMR-iKru5voI4fsJSUwvBQYhyFDrS_Ub0OMNI7N06I3gSXBgiklBY6gu6WA2KX2tUafw_31Dc6V88q837jVQma-IxUcKEwj1nFog4-nGgPPRgXAI4vcxymS1LNF6LC0NlYySWQu2CDhwUkNPB77_jxT3-11COtOMbwa01i7Ws8bCy4HgSTQeMOfQZdYY_5QjDEEYdUMIXc1k-PbDZj-ELo9yblcwA9aprnFQwHdVVomUHH_UF-LVh0DZ_GFmDQwwiNSu0w-thBBuBcDVSv1DD_OBDWi99ECIgXXAgzw5HsTjI7JzCMIFiQ0z3tpdD3F_GkkpnuWgR89n9afoCVA"
        self.executive_producer="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFHc3J4Ul9fRW4xRDFiZ2pibWF5RCJ9.eyJpc3MiOiJodHRwczovL3ppeWFkLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGZlN2VlM2Y0NjJiMjAwNzFiYTA1MjQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYzMDc4MTU1NywiZXhwIjoxNjMwODY3OTU3LCJhenAiOiJhTGVueTU5dFNGcTdlejJFQWhXbEs2QThoTHpGMVJaSiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.yvOzbULhaCCXUPPohbRE0bqoCiJwI-FREB4e0LnhLlwIw_XJLEigeSWkmnYlcbZhi2XmYUmF5mi_Kr6zjN92touMqPgIzSdbCbIGd61IFpSSHQ6n5TGPgLie3wj9s64gl6JsTWTURlGNlnrxNfox1HWhw296p1HnJShZkxP92sppcgT6kCaIeZbKcGK_FsD6kANYjMs8hTUZrW1mFwPL6xEYcgmfdvC4tH1FZiMfqHp7AMvH5uAk5xbTJJeK9T0cs8UTZOlCIeGeJeh3XLTSGnEcHg6VTRfAO44A7RXvMaPGRx2zwC0DPdpLa9LRVt1OayjiLtTIIsFuS8dBfEbMSw"

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