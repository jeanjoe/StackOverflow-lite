import unittest, json, requests
from datetime import datetime
import app

BASE_URL = 'http://127.0.0.1:5000/api/v1/questions'

question_manager = app.ManageQuestions()

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

    def test_post_question(self):
        test_data = {
            'author': 1,
            'title': 'Test Title',
            'body': 'Test text body',
            'tags': 'Test, Python'
        }
        response = requests.post(BASE_URL, params= test_data)
        #On successfull Posting, Return success must Equal 1
        return self.assertEqual(1, response.json()['success'])
    
    def test_get_specific_question(self):
        response = requests.get(BASE_URL+'/1')
        self.assertEqual(1, response.json()['success'])

    def test_delete_question(self):
        response = requests.delete(BASE_URL + '/3?author=1')
        expected_response = {
            'success': 1,
            'message': 'Question Removed successfully'
        }
        self.assertEqual(expected_response, response.json())
 
    def test_post_answer(self):
        test_data = {
            'author': 12,
            'answer': 'Test answer',
        }
        response = requests.post(BASE_URL + '/1/answers', params= test_data)
        #On successfull Posting, Return success must Equal 1
        return self.assertEqual(1, response.json()['success'])

    def teardown(self):
        # teardown here..
        question_manager.questions = self.api

if __name__ == '__main__':
    unittest.main()