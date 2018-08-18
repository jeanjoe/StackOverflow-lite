import unittest, json, requests
from datetime import datetime
from api.models import ManageQuestions

BASE_URL = 'http://127.0.0.1:5000/api/v1/questions'

question_manager = ManageQuestions()

class TestApi(unittest.TestCase):

    def setUp(self):
        self.api = question_manager.questions

    def test_get_all_question(self):
        response = requests.get(BASE_URL)
        self.assertIsInstance(response.json(), dict)

    def test_post_question(self):
        test_data = {
            'author': 1,
            'title': 'Does my post question reach the end point?',
            'body': 'Am testing my Api End point for posting Questions',
            'tags': 'Test, Python'
        }
        response = requests.post(BASE_URL, params= test_data)
        #On successfull Posting, Return success must Equal 1
        return self.assertEqual(1, response.json()['success'])
    
    def test_get_specific_question(self):
        response = requests.get(BASE_URL+'/1')
        self.assertEqual(1, response.json()['success'])
    
    def test_get_specific_question_not_found(self):
        response = requests.get(BASE_URL+'/1000')
        expected_response = {
            'success': 0,
            'message': 'Unable to find Question with ID 1000'
        }
        self.assertEqual(expected_response, response.json())

    def test_successful_delete_question(self):
        response = requests.delete(BASE_URL + '/2?author=1')
        expected_response = {
            'success': 1,
            'message': 'Question Removed successfully'
        }
        self.assertEqual(expected_response, response.json())

    def test_delete_question_not_found(self):
        response = requests.delete(BASE_URL + '/12?author=1')
        expected_response = {
            'success': 0, 
            'message': 'Unable to find Question with ID 12'
        }
        self.assertEqual(expected_response, response.json())

    def test_unauthorised_delete_question(self):
        response = requests.delete(BASE_URL + '/1?author=5')
        expected_response = {
            'success': 0, 
            'message': 'You donot have permission to delete this Question 1'
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