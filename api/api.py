from flask import Flask, jsonify, request, json
from datetime import datetime
import uuid
from .models import ManageQuestions, ManageUser, Validator

app = Flask(__name__)
question_manager = ManageQuestions()
user_manager = ManageUser()
validation = Validator()

#Test API Root Directory
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Kudos, API endpoints Work. Follow /api/v1/questions to get Questions', 
        'success': 1 
        }), 200

#Route to handle POST Question
@app.route('/api/v1/questions', methods=['POST'])
def post_question():
    #Validate user input
    validate = validation.required(['title','body','author','tags'])
    if len(validate):
        return jsonify({'success': 0, 'validation': validate}), 200
    data = request.get_json()
    if validation.unique('questions', data['title'], 'title') is not None:
        return jsonify({ 'message': 'This question has already been asked, please try another.' }), 200
    
    #Post question
    question = {
        'id' : len(question_manager.questions) + 1,
        'author': data['author'],
        'title': data['title'],
        'body': data['body'],
        'tags': data['tags'],
        'created_at': str(datetime.now())
    }    
    question_manager.questions.append(question)
    return jsonify({'success': 1, 'question': question}), 201

#Route to GET All Questions
@app.route('/api/v1/questions', methods=['GET'])
def all_questions():
    return jsonify({ 'question': question_manager.questions, 'success': 1}), 200

#Route to GET a Specific Question
@app.route('/api/v1/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    if question_manager.question_not_found(question_id) is not True:
        return question_manager.question_not_found(question_id), 404
    return jsonify({ 
        'success': 1, 
        'question' : question_manager.search_question(question_id),
        'answers' : question_manager.question_answers(question_id)
        }), 200

#Route to Delete Question
@app.route('/api/v1/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    if question_manager.question_not_found(question_id) is not True:
        return question_manager.question_not_found(question_id), 404
    #Validate Author
    validate = validation.required(['author'])
    if len(validate):
        return jsonify({'success': 0, 'validation': validate}), 200
    data = request.get_json()
    if str(data['author']) == str(question_manager.search_question(question_id)['author']):
        question_manager.questions.remove(question_manager.search_question(question_id))
        return jsonify({ 'success': 1, 'message': 'Question Removed successfully'}), 200
    return jsonify({
        'success': 0, 
        'message': 'You donot have permission to delete this Question' 
        }), 401

#Route to POST an answer to a Question
@app.route('/api/v1/questions/<question_id>/answers', methods=['POST'])
def post_answer(question_id):
    #check if question exists
    if question_manager.question_not_found(question_id) is not True:
        return question_manager.question_not_found(question_id), 404
    #Validate User Input
    validate = validation.required(['author','answer'])
    if len(validate) > 0:
        return jsonify({'success': 0, 'validation': validate}), 200

    if validation.unique('answers', request.get_json('answer'), 'answer') is not None:
        return jsonify({ 'message': 'This answer has already been given, please try another.' }), 200
    data = request.get_json()
    #Post the Answer to this Question
    response_answer = {
        'id' : str(uuid.uuid1()),
        'question_id': question_id,
        'author_id': data['author'], 
        'answer': data['answer'],
        'prefered_answer': 0, 
        'created_at': str(datetime.now())
    }    
    question_manager.answers.append(response_answer)
    return jsonify({
        'success': 1, 'message': 'Answer posted successfuly'
        }), 200

#Add User authentication endpoints
@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    #Validate User Input
    validate = validation.required(['name', 'email', 'password'])
    if len(validate) > 0:
        return jsonify({'success': 0, 'validation': validate}), 200 
    user = {
        # make a UUID based on the host ID and current time
        'id': str(uuid.uuid1()),
        'display_name': request.args['name'],
        'email': request.args['email'],
        'password': request.args['password']
    }

    user_manager.users.append(user)
    return jsonify({'user': user}), 200
