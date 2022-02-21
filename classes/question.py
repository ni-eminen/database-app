class Question:
    def __init__(self, question_string):
        self.question_string = question_string
        self.answers = []

    def add_answer(self, answer):
        self.answers.append(answer)

    def question(self):
        return self.question_string

    # return True if the answer_candidate is found within the answers for this question
    def is_correct(self, answer_candidate):
        for answer in self.answers:
            if answer == answer_candidate:
                return True
        return False