from cmd import IDENTCHARS
from flask import Flask
from flask import redirect, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import random

from flask_cors import CORS

from Questions import Questions
from Question import Question

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

# login

@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # check pass
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
  print('username: ', request.form.get('username'))
  return render_template('login.html')


# general

@app.route("/")
def index():
    quizes = db.session.execute('select * from quizes;').fetchall()
    print('-----------------', quizes)
    return render_template("frontpage.html", quizes=quizes, len=len(quizes))


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