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
    return render_template('test.html', quizname=quizname)

