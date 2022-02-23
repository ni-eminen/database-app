# Quiz app
Quiz app for University of Helsinki's database project course.

[heroku](https://matoskni-database.herokuapp.com/)

## Notes:
- Login before opening quizs. A new user will be created when you login for the first time. If the username is taken, you will be met with an error message.

## Functionalities
- Create a user
- Login
- Selection of Quizs
- Highscores
- Highscore tracking both global and user based

## Functionalities to be
- Users will be able to create new quizs

## Install & run

run the following commands:

### setting up
	source ./venv/bin/activate
	pip install -r requirements.txt
	psql < schema.sql
	psql < quizes.sql

### run flask
	[FLASK_DEBUG=1] flask run
