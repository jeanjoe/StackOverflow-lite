from flask import Flask, jsonify, request, json
from datetime import datetime

app = Flask(__name__)
questions = []

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
        if len(questions) > 0:
            last_id = questions[-1]['id']

        question = {
            'id' : last_id+1,
            'author' : 1,
            'title' : request.args['title'],
            'body' : request.args.get('body'),
            'tags' :request.args.get('tags'),
            'created_at' : str(datetime.now())
        }    
        questions.append(question)
        return jsonify({'success': 1, 'questions': question}), 201

#Route to GET All Questions
@app.route('/api/v1/questions', methods=['GET'])
def all_questions():
    return jsonify({ 'data' : questions, 'success': 1})

#Route to GET a Specific Question
@app.route('/api/v1/questions/<int:id>', methods=['GET'])
def get_question(id):
    if search_question(id) == False:
        return jsonify({ 
            'success': 0, 
            'message' : 'Unable to find Question with ID {0}'.format(id) 
            })
    return jsonify({ 'success': 1, 'question' : search_question(id) }), 200

#Route to Delete Question
@app.route('/api/v1/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    if search_question(id) == False:
        return jsonify({ 
            'success': 0, 
            'message' : 'Unable to find Question with ID {0}'.format(id) 
            })

    #Validate Author
    if request.args.get('author') is None or not request.args.get('author'):
        return jsonify({ 'success':0, 'message': 'Author ID is required'})
    if int(request.args['author']) == int(search_question(id)['author']):
        questions.remove(search_question(id))
        return jsonify({ 'success': 1, 'message': 'Question Removed successfully'}), 202
    return jsonify({'success': 0, 'message': 'You donot have permission to delete this Question {0}'.format(search_question(id)['author']) }), 401

#Method to Search for a Question and if found, return the Question else return False
def search_question(id):
    if len(questions) > 0:
        try:
            question = next( question for question in questions if question['id'] == id)
            return question
        except:
            return False
    return False

if __name__ == '__main__':
    app.run(debug=True)