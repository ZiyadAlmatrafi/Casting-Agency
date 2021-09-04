# Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
- Base URL: https://my-capstone-project-fsnd.herokuapp.com

## Getting Started:
### Installing Dependencies
Run the command
``` pip3 install -r requirements.txt ```

### Running the server
``` 
export FLASK_APP=app.py
export FLASK_ENV=development
flask run 
```
### Database Setup
Run the command to create the database``` CREATE DATABASE {DATABASE_NAME};``` 
then run these below:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
### Error Handling:
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 401,
    "message": "Unuthorized"
}
```
The API will return these error types when requests fail:
- 400: Bad Request
- 401 Unuthorized
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500 Internal server error

### Authentication
## Roles
- Casting Assistant: 
  - Can view actors and movies
- Casting Director:
  - All permissions a Casting Assistant has
  - Add or delete an actor from the database 
  - Modify actors or movies
- Executive Producer:
  - All permissions a Casting Director has
  - Add or delete a movie from the database


### Endpoints:

#### Get Movies:
`https://my-capstone-project-fsnd.herokuapp.com/movies`

Get all movies
- Returns:
```
{
    "movies": [
        {
            "id": 1,
            "release": "2/2/2019",
            "title": "Avengers: Endgame"
        },
        {
            "id": 2,
            "release": "2/2/2018",
            "title": "Avengers: Infinity War"
        }
    ],
    "success": true
}
```
#### Get Actors:
`https://my-capstone-project-fsnd.herokuapp.com/actors`

Get all actors
- Returns:
```
{
    "actors": [
        {
            "age": 36,
            "gender": "Female",
            "id": 1,
            "name": "Scarlett Johansson"
        },
        {
            "age": 25,
            "gender": "Male",
            "id": 2,
            "name": "Tom Holland"
        }
    ],
    "success": true
}
```
#### Delete a movie:
`https://my-capstone-project-fsnd.herokuapp.com/movies/1`

- Returns:
```
{
    "success": true
}
```
#### Delete an actor:
`https://my-capstone-project-fsnd.herokuapp.com/actors/1`

- Returns:
```
{
    "success": true
}
```
#### Add a movie:
`https://my-capstone-project-fsnd.herokuapp.com/add-movie`

- body:
```
{
    "title":"Avengers: Endgam",
    "release":"2/2/2019"
}
```
- Returns:
```
{
    "success": true
}
```
#### Add an actor:
`https://my-capstone-project-fsnd.herokuapp.com/add-actor`

- body:
```
{
    "name":"Scarlett Johansson",
    "age":"36",
    "gender":"Female"
}
```
- Returns:
```
{
    "success": true
}
```
#### Update a movie:
`https://my-capstone-project-fsnd.herokuapp.com/movies/2`

- body:
```
{
    "title":"free guy",
    "release": "2/2/2021"
}
```
- Returns:
```
{
    "movie": {
        "id": 2,
        "release": "2/2/2021",
        "title": "free guy"
    },
    "success": true
}
```
#### Update an actor:
`https://my-capstone-project-fsnd.herokuapp.com/actor/2`

- body:
```
{
    "name":"Tom Holland",
    "age":"33",
    "gender":"Male"
}
```
- Returns:
```
{
    "actor": {
        "age": 33,
        "gender": "Male",
        "id": 2,
        "name": "Tom Holland"
    },
    "success": true
}
```
