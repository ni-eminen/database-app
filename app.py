from flask import Flask
from flask import redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv

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
    answers_query = f"select answers.answer_string, answers.is_correct from answers, quizes, questions where " \
                    f"quizes.name='{quizname}' and questions.quiz_id=quizes.id and answers.question_id=question_id;"
    questions = db.session.execute(questions_query).fetchall()
    answers = db.session.execute(answers_query).fetchall()
    print(questions_query)
    print(questions)
    for question in questions:
        print(question)
    for answer in answers:
        print(answer)
    return render_template('test.html', quizname=quizname, questions=questions)

