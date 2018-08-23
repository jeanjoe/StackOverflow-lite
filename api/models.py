from flask import request, jsonify
from datetime import datetime

questions = []
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
    def get_a_question(self, question_ID):
        question = next((question for question in self.questions if question['id'] == question_ID), None)
        return question

    #Get last id of Datalists
    def last_id(self, search_type):
        if search_type == 'answers':
            return self.answers[-1]['id'] if len(self.answers) > 0 else  0
        if len(self.questions) > 0:
            return self.questions[-1]['id']
        return  0

    #If Question not found, return this error
    def search_question(self, question_id):
        if self.get_a_question(question_id) == None:
            return jsonify({ 
                'success': 0, 
                'message' : 'Unable to find Question with ID {0}'.format(question_id) 
                })
        return True

#User class
class ManageUser():
    def __init__(self, users = []):
        self.users = users

    def get_user(self):
        return jsonify({ 'users': 'manzede'})

class Validator():
    def __init__(self):
        self.questions = questions
        self.answers = answers
        
    #Validate User Inputs
    def required(self, data = []):
        error_message = []
        for i in data:
            if request.args.get(i) is None or not request.args.get(i):
                error_message.append({ 'field' : i, 'message': i + ' is required' })
        #return errors
        return error_message
    
    def unique(self, search_from, data, field):
        list_holder = self.questions
        if search_from =='answers':
            list_holder = self.answers
        return next((item for item in list_holder if item[field] == data), None)