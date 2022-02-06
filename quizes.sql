insert into quizes (name, description, url) values ('sql-quiz', 'This quiz will quiz you on your sql expertise!', 'sql-quiz');
insert into quizes (name, description, url) values ('generic quiz', 'This quiz will quiz you about something that is yet to be decided...', 'generic-quiz');
insert into quizes (name, description, url) values ('generic quiz', 'This quiz will quiz you about something that is yet to be decided...', 'generic-quiz');

insert into questions (question_string, quiz_id) values ('Who invented sql', 1);
insert into questions (question_string, quiz_id) values ('What is nosql?', 1);
insert into questions (question_string, quiz_id) values ('What are sqls benefits over nosql', 1);
insert into questions (question_string, quiz_id) values ('Are we living in a simulation conducted by superintelligence?', 1);

insert into answers (answer_string, question_id, is_correct) values ('Donald D. Chamberlin and Raymond F. Boyce', 1, 1);
insert into answers (answer_string, question_id, is_correct) values ('Evan Handler', 1, 0);
insert into answers (answer_string, question_id, is_correct) values ('Wayne Gretzky', 1, 0);
insert into answers (answer_string, question_id, is_correct) values ('Steven Weber', 1, 0);

insert into answers (answer_string, question_id, is_correct) values ('A NoSQL database provides a mechanism for storage and retrieval of data that is modeled in means other than the tabular relations used in relational databases.', 2, 1);
insert into answers (answer_string, question_id, is_correct) values ('A style sheet language used for describing the presentation of a document written in a markup language such as HTML.', 2, 0);
insert into answers (answer_string, question_id, is_correct) values ('A set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.', 2, 0);
insert into answers (answer_string, question_id, is_correct) values ('An open-source, cross-platform, back-end JavaScript runtime environment that runs on the V8 engine and executes JavaScript code outside a web browser.', 2, 0);

insert into answers (answer_string, question_id, is_correct) values ('SQL databases are better for multi-row transactions', 3, 1);
insert into answers (answer_string, question_id, is_correct) values ('SQL databases are horizontally scalable.', 3, 0);
insert into answers (answer_string, question_id, is_correct) values ('SQL databases are non-relational.', 3, 0);
insert into answers (answer_string, question_id, is_correct) values ('SQL is better for unstructured data like documents or JSON.', 3, 0);

insert into answers (answer_string, question_id, is_correct) values ('Yes', 4, 1);
insert into answers (answer_string, question_id, is_correct) values ('Probably', 4, 1);
insert into answers (answer_string, question_id, is_correct) values ('Probability is low', 4, 1);
insert into answers (answer_string, question_id, is_correct) values ('Depends on the parallel universe', 4, 1);