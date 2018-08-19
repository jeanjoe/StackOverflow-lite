from datetime import datetime

questions = [
    {
        "author": 1,
        'title': 'Does my first Mock Test title Work?',
        'body': 'Mocking second Test body Text',
        "created_at": str(datetime.now()),
        "id": 1,
        "tags": "html, test, python",
    },
    {
        "author": 1,
        'title': 'Second Mock Test title seems not Working',
        'body': 'Mocking second Test body Text',
        "created_at": str(datetime.now()),
        "id": 2,
        "tags": "html, test, python",
    }
]
answers = []

class ManageQuestions():
    def __init__(self):
        self.questions = questions
        self.answers = answers
    
    #Method to search for Question Answers if found, return question and answers else return False
    def question_answers(self, question_ID):
        searched_answers = []
        if self.search_question != False or not self.search_question != None:
            if len(self.answers) > 0:
                for i in self.answers:
                    if i['question_id'] == question_ID: searched_answers.append(i)
        return searched_answers
            
    #Method to Search for a Question and if found, return the Question else return False
    def search_question(self, question_ID):
        if len(self.questions) > 0:
            question = next((question for question in self.questions if question['id'] == question_ID), None)
            return question
        return False