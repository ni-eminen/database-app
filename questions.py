"""A module for a class containing all the questions in a Quiz"""
from question import Question

class Questions:
    """Questions class"""
    def __init__(self):
        """Init questions array"""
        self.questions = []

    def add_question(self, new_question):
        """Add a Question to the set, parse out potential duplicates"""
        # for all questions in this collection
        for ques in self.questions:
            # if question is already in collection
            if ques.question_string == new_question.question_string:
                # check that all the answers are in the collection as well, if
                # not, add the new answers
                for ans in new_question.answers:
                    if not ans in ques.answers:
                        ques.add_answer(ans)
                # return false to inform question was already in the collection
                return False
        # else append the collection with the new question
        self.questions.append(new_question)
        return True

    # returns true if the given answer is correct to the given question
    def is_correct(self, question_, answer):
        """return if an answer is correct or not to a specific question"""
        question_ = list(
            filter(
                lambda x: x.question_string == question_,
                self.questions))[0]
        return question_.is_correct(answer)


questions = Questions()
question = Question('what?')
question.add_answer('yes')
questions.add_question(question)
print(questions.is_correct('what?', 'yes'))
