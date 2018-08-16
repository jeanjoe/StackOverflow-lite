from flask import Flask, jsonify

app = Flask(__name__)

#Test API Root Directory
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Kudos, API endpoints Work. Follow /api/v1/questions to get Questions', 
        'success': 1 
        })

if __name__ == '__main__':
    app.run(debug=True)