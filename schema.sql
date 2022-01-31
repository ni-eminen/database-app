CREATE TABLE quizes (id SERIAL PRIMARY KEY, name TEXT, description TEXT, url TEXT);
CREATE TABLE questions (id SERIAL PRIMARY KEY, question_string TEXT);
CREATE TABLE answers (id SERIAL PRIMARY KEY, answer_string TEXT, CONSTRAINT question_id FOREIGN KEY (id) REFERENCES questions (id), is_correct INTEGER);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE scores (id SERIAL PRIMARY KEY, CONSTRAINT user_id FOREIGN KEY (id) REFERENCES users (id), score INTEGER, CONSTRAINT quiz_id FOREIGN KEY (id) REFERENCES quizes (id))
