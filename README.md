# Quiz app
Quiz app for University of Helsinki's database project course.

[heroku](https://matoskni-database.herokuapp.com/)

## Functionalities (to be)
- Create a user
- Selection of Quiz's
- Highscore tracking both global and user based

## Install & run

run the following commands:

### setting up
	source ./venv/bin/activate
	pip install -r requirements.txt
	psql < schema.sql
	psql < quizes.sql

### run flask
	[FLASK_DEBUG=1] flask run
