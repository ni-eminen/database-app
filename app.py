from flask import Flask
from flask import redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import random

from Questions import Questions
from Question import Question

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


@app.route("/")
def index():
    # db.session.execute("INSERT INTO visitors (time) VALUES (NOW())")
    # db.session.commit()
    # result = db.session.execute("SELECT COUNT(*) FROM visitors")
    # counter = result.fetchone()[0]

    quizes = db.session.execute('select * from quizes;').fetchall()
    print('-----------------', quizes)
    return render_template("frontpage.html", quizes=quizes, len=len(quizes))


@app.route('/quiz/<string:quizname>')
def quiz(quizname):
    questions_query = f"select questions.question_string from quizes, questions where name='{quizname}' " \
                                                                                f"AND questions.quiz_id=quizes.id;"
    answers_query = f"select answers.answer_string from answers, quizes, questions where " \
                    f"quizes.name='{quizname}' and questions.quiz_id=quizes.id and answers.question_id=questions.id;"
    questions = db.session.execute(questions_query).fetchall()
    answers = db.session.execute(answers_query).fetchall()
    print(questions_query)
    print(questions)
    for question in questions:
        print(question)
    for answer in answers:
        print(answer)
    if len(questions) == 0:
        return render_template('quiz_not_ready.html', quizname=quizname)
    return render_template('quiz.html', quizname=quizname, questions=questions, answers=answers, answerslen=len(answers),
                            questionslen=len(questions))

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
    db.session.commit();
    return jsonify(id=id)

@app.route('/quiz/results/<string:id>')
def result(id):
    score = db.session.execute('select score from scores;').fetchone()[0]
    print(score)
    return render_template('results.html', score = score)



# db functions

def get_questions(quizname):
    questions_query = f"select questions.question_string from quizes, questions where name='{quizname}' " \
                                                                            f"AND questions.quiz_id=quizes.id;"
    return db.session.execute(questions_query).fetchall()

def get_correct_answers(quizname):
    answers_query = f"select questions.question_string, answers.answer_string from answers, quizes, questions where " \
                    f"quizes.name='{quizname}' and questions.quiz_id=quizes.id and answers.question_id=questions.id AND answers.is_correct=1;"
    return db.session.execute(answers_query).fetchall()

def get_answers(quizname):
    answers_query = f"select answers.answer_string from answers, quizes, questions where " \
                    f"quizes.name='{quizname}' and questions.quiz_id=quizes.id and answers.question_id=questions.id;"
    return db.session.execute(answers_query).fetchall()