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
        return jsonify({'success': 1, 'data': question}), 201

if __name__ == '__main__':
    app.run(debug=True)