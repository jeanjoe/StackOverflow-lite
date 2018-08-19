from flask import request, jsonify
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
        for i in self.answers:
            if i['question_id'] == question_ID: searched_answers.append(i)
        return searched_answers
            
    #Method to Search for a Question and if found, return the Question else return False
    def search_question(self, question_ID):
        question = next((question for question in self.questions if question['id'] == question_ID), None)
        return question

    def last_id(self, search_type):
        if search_type == 'answers':
            return self.answers[-1]['id'] if len(self.answers) > 0 else  0
        return self.questions[-1]['id'] if len(self.questions) > 0 else  0

    def validate(self, data):
        if request.args.get(data) is None or not request.args.get(data):
            return jsonify({ 'success':0, 'message': data + ' is required'})
        return True

    def question_not_found(self, question_id):
        if self.search_question(question_id) == None:
            return jsonify({ 
                'success': 0, 
                'message' : 'Unable to find Question with ID {0}'.format(question_id) 
                })
        return True