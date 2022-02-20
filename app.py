from curses import REPORT_MOUSE_POSITION
from flask import Flask, redirect, render_template, request, jsonify, session
from urllib.parse import urlparse, urljoin
import flask as flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import uuid
from database import Database

# flask plugins
from flask_login import LoginManager, login_user, login_required, logout_user, current_user 
from flask_cors import CORS
from flask_bootstrap import Bootstrap

# user authentication
from werkzeug.security import generate_password_hash, check_password_hash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

# user classes
from questions import Questions
from question import Question
from user import User

# app object
app = Flask(__name__)
login_manager = LoginManager()
CORS(app)
Bootstrap(app)
login_manager.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
database_class = Database(app)
db = database_class.get_db()


# LoginForm class
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

# login

@app.route('/loginpage', methods=['GET', 'POST'])
def login_page():
  form = LoginForm()
  return flask.render_template('login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  #authentication
  username = request.form.get('username')
  password = request.form.get('password')

  db_user = db.session.execute(f"select * from users where username='{username}';").fetchone()
  
  if not db_user:
    print('creating new user')
    user = create_user(username, password)
  else:
    user = User(db_user[1], db_user[0])





  login_user(user)
  return redirect('/')

@app.route("/logout")
@login_required
def logout():
  print(current_user.is_authenticated)
  logout_user()
  return redirect('/')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
          ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(user_id):
  return User.get(user_id)


# general

@app.route("/")
def index():
  quizes = db.session.execute('select * from quizes;').fetchall()
  print('-----------------', quizes)
  return render_template("frontpage.html", quizes=quizes, len=len(quizes), current_user=current_user)


@app.route('/quiz/<string:quizname>')
@login_required
def quiz(quizname):
  questions = get_questions_with_answer_count(quizname)
  answers = get_answers(quizname)

  if len(questions) == 0:
    return render_template('quiz_not_ready.html', quizname=quizname)
  
  # qna will be and array of arrays, each sub array represents a question and its answers, each node in string format
  qna = []

  # for each question, add the question_string into an array, then append that array 
  # with the questions that have the appropriate question id
  for q in questions:
    arr = [q[0]]
    for a in answers:
      if q[1] == a[1]:
        arr.append(a[0])
    qna.append(arr)

  return render_template('quiz.html', quizname=quizname, qna=qna, questions=questions, answers=answers, answerslen=len(answers),
                          questionslen=len(questions))

@app.route('/quiz/results/<string:id>')
def result(id):
  score = db.session.execute(f'select score, quiz_id from scores where id={id};').fetchone()
  print('scoreeeeeeeeeeeeeeeeeee',score)
  name = get_quiz_name(score[1])
  return render_template('results.html', score = score[0], name=name)


@app.route('/quiz/submit', methods = ['POST', 'GET'])
def submit():
  body = request.form
  quizname = body['quizname']
  questions_answers = get_correct_answers(quizname)

  # Add questions and correct answers to an object that is easily querable
  questions = Questions()
  for qna in questions_answers:
      q = Question(qna[0])
      q.add_answer(qna[1])
      questions.add_question(q)

  # Create an array of type [(question, given answer, correct or not)]
  result_list = []
  answer_list = []
  score = 0
  for question in questions_answers:
      # Duplicate answers sometimes result from multiple correct answers, skip them via this statement
      q = question[0] # question
      a = body[q]     # answer
      if a in answer_list:
          continue

      answer_list.append(a)

      if questions.is_correct(q, body[q]):
          result_list.append((q, body[q], True))
          score = score + 1
      else:
          result_list.append((q, body[q], False))

  quiz_id = get_quiz_id_by_name(quizname)
  # generate id for this quiz session
  response = db.session.execute(f"INSERT INTO scores (score, quiz_id, user_id) VALUES ({score}, {quiz_id}, {current_user.get_id()}) RETURNING id;")

  print('scores after insertr',db.session.execute('select * from scores;').fetchall())
  db.session.commit()
  return jsonify(id=response.fetchone()[0])


@app.route('/profile')
def profile():
  if not current_user.is_authenticated:
    return redirect('/loginpage')
  
  scores = get_scores(current_user.get_id())

  quiz_names_and_scores = []
  for score in scores:
    name = get_quiz_name(score[3])
    quiz_names_and_scores.append([name, score[2]])

    print(quiz_names_and_scores)

  return render_template('profile.html', current_user=current_user, scores=quiz_names_and_scores)


# db functions

def get_questions(quizname):
  questions_query = f"select questions.question_string from quizes, questions where name='{quizname}' " \
                    f"AND questions.quiz_id=quizes.id;"
  return db.session.execute(questions_query).fetchall()

def get_questions_with_answer_count(quizname):
  questions_query =   f"select questions.question_string, questions.id, count(*) from quizes, questions, answers where"\
                      f" questions.id=answers.question_id and quizes.name='{quizname}' group by questions.question_string, questions.id;"
  return db.session.execute(questions_query).fetchall()

def get_correct_answers(quizname):
  answers_query = f"select questions.question_string, answers.answer_string from answers, quizes, questions where " \
                  f"quizes.name='{quizname}' and questions.quiz_id=quizes.id and answers.question_id=questions.id AND answers.is_correct=1;"
  return db.session.execute(answers_query).fetchall()

def get_answers(quizname):
  answers_query = f"select answers.answer_string, answers.question_id from answers, quizes, questions where " \
                  f"quizes.name='{quizname}' and questions.quiz_id=quizes.id and answers.question_id=questions.id;"
  return db.session.execute(answers_query).fetchall()

def get_choice_count_for_question(question_id):
  query = f"SELECT COUNT(*) FROM answers WHERE answer.id={question_id}"

def create_user(username, password):
  password_hash = generate_password_hash(password, method='sha256')
  query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password_hash}');"
  db.session.execute(query)
  user_id = db.session.execute(f"SELECT id FROM users where username='{username}';").fetchone()[0]
  db.session.commit()
  return User.get(user_id)

def get_user_id(username):
  query = f"SELECT id FROM users WHERE username='{username}';"
  id = db.session.execute(query).fetchone()[0]
  print(id)
  return id

def get_scores(user_id):
  query = f"SELECT * FROM scores WHERE user_id='{user_id}'"
  scores = db.session.execute(query).fetchall()
  print('scores', scores)
  return scores

def get_quiz_name(quiz_id):
  query = f"SELECT name FROM quizes WHERE id={quiz_id};"
  print('finding name for', query)
  response = db.session.execute(query).fetchone()
  if response:
    name = response[0]
  else:
    name = 'no name found'
  return name

def get_quiz_id_by_name(name):
  query = f"SELECT id FROM quizes WHERE name='{name}';"
  id = db.session.execute(query).fetchone()[0]
  return id 