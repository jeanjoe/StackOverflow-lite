from flask import Flask, jsonify, request, json
from datetime import datetime
from .models import ManageQuestions

app = Flask(__name__)
question_manager = ManageQuestions()

#Test API Root Directory
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Kudos, API endpoints Work. Follow /api/v1/questions to get Questions', 
        'success': 1 
        })

#Route to handle POST Question
@app.route('/api/v1/questions', methods=['POST'])
def save_question():
    if request.args.get('title') is None or not request.args.get('title'):
        return jsonify({ 'success':0, 'message': 'Title field is required'})
    elif request.args.get('body') is None or not request.args.get('body'):
        return jsonify({ 'success': 0, 'message': 'Body is required'})
    else:
        last_id = 0
        if len(question_manager.questions) > 0:
            last_id = question_manager.questions[-1]['id']

        question = {
            'id' : last_id+1,
            'author' : 1,
            'title' : request.args['title'],
            'body' : request.args.get('body'),
            'tags' :request.args.get('tags'),
            'created_at' : str(datetime.now())
        }    
        question_manager.questions.append(question)
        return jsonify({'success': 1, 'questions': question}), 201

#Route to GET All Questions
@app.route('/api/v1/questions', methods=['GET'])
def all_questions():
    return jsonify({ 'data' : question_manager.questions, 'success': 1})

#Route to GET a Specific Question
@app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    if question_manager.search_question(question_id) == False or question_manager.search_question(question_id) == None:
        return jsonify({ 
            'success': 0, 
            'message' : 'Unable to find Question with ID {0}'.format(question_id) 
            })
    return jsonify({ 
        'success': 1, 
        'question' : question_manager.search_question(question_id),
        'answers' : question_manager.question_answers(question_id)
        }), 200

#Route to Delete Question
@app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    if question_manager.search_question(question_id) == False or question_manager.search_question(question_id) == None:
        return jsonify({ 
            'success': 0, 
            'message' : 'Unable to find Question with ID {0}'.format(question_id) 
            })
    #Validate Author
    if request.args.get('author') is None or not request.args.get('author'):
        return jsonify({ 'success':0, 'message': 'Author ID is required'})
    if int(request.args['author']) == int(question_manager.search_question(question_id)['author']):
        question_manager.questions.remove(question_manager.search_question(question_id))
        return jsonify({ 'success': 1, 'message': 'Question Removed successfully'}), 202
    return jsonify({
        'success': 0, 
        'message': 'You donot have permission to delete this Question {0}'.format(question_manager.search_question(question_id)['author']) }), 401

#Route to POST an answer to a Question
@app.route('/api/v1/questions/<int:question_id>/answers', methods=['POST'])
def post_answer(question_id):
    if question_manager.search_question(question_id) == False or question_manager.search_question(question_id) == None:
        return jsonify({ 
            'success': 0, 
            'message' : 'Unable to find Question with ID {0}'.format(question_id) 
            })
    #Validate User Input
    if request.args.get('author') is None or not request.args.get('author'):
        return jsonify({ 'success':0, 'message': 'Author ID is required'})
    if request.args.get('answer') is None or not request.args.get('answer'):
        return jsonify({ 'success': 0, 'message': 'Answer is required'})
    
    #Post the Answer to this Question
    last_id = question_manager.answers[-1]['id'] if len(question_manager.answers) > 0 else  0
    answer = {
        'id' : last_id+1,
        'question_id': question_manager.search_question(question_id)['id'],
        'author_id': request.args['author'], 'answer': request.args['answer'],
        'prefered_answer': False, 'created_at': str(datetime.now())
    }    
    question_manager.answers.append(answer)
    return jsonify({
        'success': 1, 'answer': answer, 'message': 'Answer posted successfuly'
        })