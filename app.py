from models import Actor, Movie, setup_db, db_drop_and_create_all
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import  requires_auth, AuthError
import sys
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  #db_drop_and_create_all()

  #Get movies
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(payload):
      try:
        movies = Movie.query.all()
        formated_movies = [movie.format() for movie in movies]
      except BaseException:
          print(sys.exc_info())
          abort(422)  
      return jsonify({
        "success": True,
        "movies": formated_movies
    })
  #Get actors 
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(payload):
      actors = Actor.query.all()
      formated_actors = [actor.format() for actor in actors]
      return jsonify({
        "success": True,
        "actors": formated_actors
    })
  
  #Delete a movie
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
      try:
          movie = Movie.query.filter(Movie.id == id).one_or_none()

          if movie is None:
              abort(404)

          movie.delete()
      except:
          abort(404)

      return jsonify({
          "success": True
      })

  #Delete an actor
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
      try:
          actor = Actor.query.filter(Actor.id == id).one_or_none()

          if actor is None:
              abort(404)

          actor.delete()
      except:
          abort(404)

      return jsonify({
          "success": True
      })

  #Post a movie
  @app.route('/add-movie', methods=['POST'])
  @requires_auth('post:movies')
  def post_movie(payload):
    body = request.get_json()
    try:
        movie = Movie(
                title=body['title'],
                release=body['release']
            )
        movie.insert()
    except BaseException:
        abort(500)

    return jsonify({
        "success": True
    })

  #Post an actor
  @app.route('/add-actor', methods=['POST'])
  @requires_auth('post:actors')
  def post_actor(payload):
    body = request.get_json()
    try:
        actor = Actor(
                name=body['name'],
                age=body['age'],
                gender=body['gender']
            )
        actor.insert()
    except BaseException:
        abort(500)

    return jsonify({
        "success": True
    })
    

  #Update a movie
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, id):
    body = request.get_json()
    try:
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        movie.title = body.get('title')
        movie.release = body.get('release')
        movie.update()

    except Exception:
        abort(404)

    return jsonify({
        "success": True,
        "movie": movie.format()
    })

  #Update an actor
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, id):
    body = request.get_json()
    try:
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        actor.name = body.get('name')
        actor.age = body.get('age')
        actor.gender = body.get('gender')
        actor.update()

    except Exception:
        abort(404)

    return jsonify({
        "success": True,
        "actor": actor.format()
    })


  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

  @app.errorhandler(404)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

  @app.errorhandler(405)
  def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405


  @app.errorhandler(AuthError)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


  
  return app



app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
