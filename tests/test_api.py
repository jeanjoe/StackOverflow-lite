import unittest, json, requests
from datetime import datetime
import api

BASE_URL = 'http://127.0.0.1:5000/api/v1/questions'

question_manager = api.ManageQuestions()

question_data = [
    {
        'id': 1000,
        'author': 5,
        'title': 'Mocking Test title',
        'body': 'Mocking Test body Text',
        'created_at': str(datetime.now()),
        'tags': 'Test, Python'
    },
    {
        'id': 2000,
        'author': 5,
        'title': 'Mocking Test title',
        'body': 'Mocking Test body Text',
        'created_at': str(datetime.now()),
        'tags': 'Test, Python'
    }
]

class TestApi(unittest.TestCase):

    def setUp(self):
        self.api = question_manager.questions

    def test_get_all_question(self):
        response = requests.get(BASE_URL)
        self.assertIsInstance(response.json(), dict)

if __name__ == '__main__':
    unittest.main()