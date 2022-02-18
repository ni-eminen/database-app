from Question import Question
class Questions:
    def __init__(self):
        self.questions = []

    def add_question(self, question):
        # for all questions in this collection
        for q in self.questions:
            # if question is already in collection
            if q.question_string == question.question_string:
                # check that all the answers are in the collection as well, if not, add the new answers
                for a in question.answers:
                    if not (a in q.answers):
                        q.add_answer(a)
                # return false to inform question was already in the collection
                return False
        # else append the collection with the new question
        self.questions.append(question)
        return True

    # returns true if the given answer is correct to the given question
    def is_correct(self, question, answer):
        question = list(filter(lambda x: x.question_string == question, self.questions))[0]
        return question.is_correct(answer)


questions = Questions()
question = Question('what?')
question.add_answer('yes')
questions.add_question(question)
print(questions.is_correct('what?', 'yes'))

