# Working with OMDB API

This is a simple project which extracts 100 movie data from the OMDB API, saves it into database and work with the data using REST APIs.
It provides django command to extract data from OMDB API.

## Technologies

- Python (3.7+)
- Django (4.2+)
- Django Rest Framework (v3.14)
- Unittest
- Docker

## Installation

The only thing you need to run the project locally is **Docker**. To install it [See](https://www.docker.com/)

When you have docker installed, go to project directory and run the following command:

```
docker-compose build --no-cache
docker-compose up
```

The first command will build a Docker images from Dockerfile, the second one will run it in container.

It will run application on host `127.0.0.1:8000`

## Usage

Application consists of 2 parts: Extracting movie's data using OMDB API and CRUD operations on data in database.

### Extract Data and Save in DB

To extract data and save it in database, there is a django command called `extractmovies`. To run it go to docker container terminal and run

```
python manage.py extractmovies
```

In the project files there is a `movies.csv`. It contains 100 movies with titles and imdb ids. I have created it to make it easier getting data from OMDB.
`extractmovies` command will go through the csv file movies and do request to OMDB API. When data is collected it will save whole data into database. 
This will work only when the database is empty.

### CRUD with REST API

Project uses Django Rest Framework to provide an API wich allows all the CRUD operations on data. Some of the API methods are protected by permission.

- `GET` - available for all users
- `POST`, `PUT`, `PATCH` - available only for the authenticated users
- `DELETE` - available only for the authorized users

To access the API, just open the url in your browser: [Browsable API](http://127.0.0.1:8000/movies/)

API provides *filtering*. It is possible to filter/search movie by title. For that just provide `?title` query parameter.

API provides *pagination*. By default page size is 10, but it can be changed by providing `?page_size` query parameter.

Authenticated users can also add new movie in database by providing `title` attribute in the request data. In this case all movie details will be fetched from OMDB API and saved in the database.

### Create test user

There is another Django command to create a test user for accessing all the functionality of the API. For that you need to go to docker container terminal and run

```
python manage.py create_user
```

or

```
python manage.py shell
```

and create the user manually using django shell.

`create_user` command will create a test user with the username `test_user` and password `testuser123` and will give a permission to delete movie from the database.
You can login with the created user in you browsable API and use it.

**Please note** that this user is only a **test** user to give you a quick access to the API. You can create super user using `manage.py` and manage your users, create as many user as you want and give as much permissions as you want.

## Testing

There are unit tests for each method of API. To run them use the command `python manage.py test tests`

Enjoy!

## Contact

**Author**: Shushan Hovhannisyan

**Email**: shushhovhannisyan@gmail.com
