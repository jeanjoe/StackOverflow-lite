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

    #Post question
    last_id = question_manager.last_id('questions')
    question = {
        'id' : last_id+1,
        'author': request.args['author'],
        'title': request.args['title'],
        'body': request.args['body'],
        'tags':request.args['tags'],
        'created_at': str(datetime.now())
    }    
    question_manager.questions.append(question)
    return jsonify({'success': 1, 'question': question}), 201

#Route to GET All Questions
@app.route('/api/v1/questions', methods=['GET'])
def all_questions():
    return jsonify({ 'question': question_manager.questions, 'success': 1}), 200

#Route to GET a Specific Question
@app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    if question_manager.question_not_found(question_id) is not True:
        return question_manager.question_not_found(question_id), 404
    return jsonify({ 
        'success': 1, 
        'question' : question_manager.search_question(question_id),
        'answers' : question_manager.question_answers(question_id)
        }), 200

#Route to Delete Question
@app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    if question_manager.question_not_found(question_id) is not True:
        return question_manager.question_not_found(question_id), 404
    #Validate Author
    if request.args.get('author') is None or not request.args.get('author'):
        return jsonify({ 'success':0, 'message': 'Author ID is required'})
    if int(request.args['author']) == int(question_manager.search_question(question_id)['author']):
        question_manager.questions.remove(question_manager.search_question(question_id))
        return jsonify({ 'success': 1, 'message': 'Question Removed successfully'}), 200
    return jsonify({
        'success': 0, 
        'message': 'You donot have permission to delete this Question {0}'.format(question_manager.search_question(question_id)['author']) 
        }), 401

#Route to POST an answer to a Question
@app.route('/api/v1/questions/<int:question_id>/answers', methods=['POST'])
def post_answer(question_id):
    #check if question exists
    if question_manager.question_not_found(question_id) is not True:
        return question_manager.question_not_found(question_id), 404
    #Validate User Input
    validate = validation.required(['author','answer'])
    if len(validate) > 0:
        return jsonify({'success': 0, 'validation': validate}), 200
    
    #Post the Answer to this Question
    last_id = question_manager.last_id('answers')
    answer = {
        'id' : last_id+1,
        'question_id': question_manager.search_question(question_id)['id'],
        'author_id': request.args['author'], 'answer': request.args['answer'],
        'prefered_answer': False, 'created_at': str(datetime.now())
    }    
    question_manager.answers.append(answer)
    return jsonify({
        'success': 1, 'answer': answer, 'message': 'Answer posted successfuly'
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
        'id': uuid.uuid1(),
        'display_name': request.args['name'],
        'email': request.args['email'],
        'password': request.args['password']
    }

    user_manager.users.append(user)
    return jsonify({'user': user})