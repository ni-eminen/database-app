"""Module for all the database functions"""
import os
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash


# user classes
from user import User

# print(os.environ)
engine = create_engine(os.getenv("DATABASE_URL"))


# db functions

def get_questions(quizname):
    """Gets all the questions for quizname"""
    questions_query = f"select questions.question_string from \
                        quizes, questions where name='{quizname}' \
                        AND questions.quiz_id=quizes.id;"
    return engine.execute(questions_query).fetchall()


def get_questions_with_answer_count(quizname):
    """Gets questions with how many answers there are to each question"""
    questions_query = f"select questions.question_string, questions.id, count(*) \
      from quizes, questions, answers where questions.id=answers.question_id \
      and quizes.name='{quizname}' group by questions.question_string, questions.id;"
    return engine.execute(questions_query).fetchall()


def get_correct_answers(quizname):
    """Gets correct answers to quizname"""
    answers_query = f"select questions.question_string, answers.answer_string from answers, \
      quizes, questions where quizes.name='{quizname}' and questions.quiz_id=quizes.id and \
      answers.question_id=questions.id AND answers.is_correct=1;"
    return engine.execute(answers_query).fetchall()


def get_answers(quizname):
    """gets all answers to quiz"""
    answers_query = f"select answers.answer_string, answers.question_id from \
      answers, quizes, questions where quizes.name='{quizname}' and \
      questions.quiz_id=quizes.id and answers.question_id=questions.id;"
    return engine.execute(answers_query).fetchall()


def create_user(username, password):
    """Creates a new user"""
    password_hash = generate_password_hash(password, method='sha256')
    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password_hash}');"
    engine.execute(query)
    user_id = engine.execute(
        f"SELECT id FROM users where username='{username}';").fetchone()[0]
    # engine.commit()
    return User.get(user_id)


def get_user_id(username):
    """gets a user id by username"""
    query = f"SELECT id FROM users WHERE username='{username}';"
    user_id = engine.execute(query).fetchone()[0]
    print(user_id)
    return user_id


def get_scores(user_id):
    """Gets users scores"""
    query = f"SELECT * FROM scores WHERE user_id='{user_id}'"
    scores = engine.execute(query).fetchall()
    print('scores', scores)
    return scores


def get_all_scores():
    """Gets all scores on record"""
    query = "SELECT user_id, quiz_id, score FROM scores ORDER BY score DESC;"
    scores = engine.execute(query).fetchall()
    return scores


def get_quiz_name(quiz_id):
    """gets quiz name by its id"""
    query = f"SELECT name FROM quizes WHERE id={quiz_id};"
    print('finding name for', query)
    response = engine.execute(query).fetchone()
    if response:
        name = response[0]
    else:
        name = 'no name found'
    return name


def get_quiz_id_by_name(name):
    """gets quiz id by its name"""
    query = f"SELECT id FROM quizes WHERE name='{name}';"
    quiz_id = engine.execute(query).fetchone()[0]
    return quiz_id


def get_username_by_id(user_id):
    """gets username by id"""
    query = f"SELECT username FROM users WHERE id={user_id}"
    username = engine.execute(query).fetchone()[0]
    return username
