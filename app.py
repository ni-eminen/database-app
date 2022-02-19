from cmd import IDENTCHARS
from flask import Flask, redirect, render_template, request, jsonify, session
from urllib.parse import urlparse, urljoin
import flask as flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import random
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_cors import CORS

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# user classes
from Questions import Questions
from Question import Question

from User import User

app = Flask(__name__)
login_manager = LoginManager()
CORS(app)
login_manager.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)


# LgoinForm class
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

# login

@app.route('/loginpage', methods=['GET', 'POST'])
def login_page():
  # Here we use a class of some kind to represent and validate our
  # client-side form data. For example, WTForms is a library that will
  # handle this for us, and we use a custom LoginForm to validate.
  print('\n\n\n\n')
  form = LoginForm()
  # if form.validate_on_submit():
  #     # Login and validate the user.
  #     # user should be an instance of your `User` class
  #     print('logged in succesfully?: ', login_user(User(username='root', email='root')))

  #     flask.flash('Logged in successfully.')

  #     next = flask.request.args.get('next')
  #     # is_safe_url should check if the url is safe for redirects.
  #     # See http://flask.pocoo.org/snippets/62/ for an example.
  #     if not is_safe_url(next):
  #         return flask.abort(400)

      # return flask.redirect(next or flask.url_for('frontpage.html'))
  return flask.render_template('login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  #authentication
  print('success login:', login_user(User(request.form['username'], 'fake@email.com')))
  return redirect('/')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
          ref_url.netloc == test_url.netloc

@app.route("/logout")
def logout():
  del session["username"]
  return redirect("/")

@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
  print('username: ', request.form.get('username'))
  return render_template('login.html')

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
  score = db.session.execute(f'select score from scores where id={id};').fetchone()[0]
  return render_template('results.html', score = score)


@app.route('/quiz/submit', methods = ['POST', 'GET'])
def submit():
  body = request.form
  questions_answers = get_correct_answers(body['quizname'])

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

  print('requestrequestrequestrequestrequestrequestrequestrequestrequestrequestrequest \n\n')
  print(result_list)
  print('\n\nrequestrequestrequestrequestrequestrequestrequestrequestrequestrequestrequest')

  # generate id for this quiz session
  id = random.randint(1, 10000000)
  print(id)
  db.session.execute(f'INSERT INTO scores (id, score) VALUES ({id}, {score});')
  print('scores after insertr',db.session.execute('select * from scores;').fetchall())
  db.session.commit()
  return jsonify(id=id)


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