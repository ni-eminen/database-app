"""Module for a question that is easily queried when \
    calculating whether an answer is correct or not"""
class Question:
    """Class for a question"""
    def __init__(self, question_string):
        self.question_string = question_string
        self.answers = []

    def add_answer(self, answer):
        """Add a correct answer to this question"""
        self.answers.append(answer)

    def question(self):
        """return the questions itself as string"""
        return self.question_string

    # return True if the answer_candidate is found within the answers for this
    # question
    def is_correct(self, answer_candidate):
        """Return a bool depending on if the answer is correct or not"""
        for answer in self.answers:
            if answer == answer_candidate:
                return True
        return False
