CREATE TABLE quizes (id SERIAL PRIMARY KEY, name TEXT, description TEXT, url TEXT);
CREATE TABLE questions (id SERIAL PRIMARY KEY, question_string TEXT, quiz_id INTEGER, FOREIGN KEY (quiz_id) REFERENCES quizes(id));
CREATE TABLE answers (id SERIAL PRIMARY KEY, answer_string TEXT, question_id INTEGER, FOREIGN KEY (question_id) REFERENCES questions(id), is_correct INTEGER);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE scores (id SERIAL PRIMARY KEY, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id), score INTEGER, quiz_id INTEGER, FOREIGN KEY (quiz_id) REFERENCES quizes(id));
