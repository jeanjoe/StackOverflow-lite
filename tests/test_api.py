import unittest, json, requests
from loremipsum import get_sentence
from datetime import datetime
from api.models import ManageQuestions
import app

# BASE_URL = 'http://127.0.0.1:5000/api/v1/questions'
BASE_URL = 'https://manzede-stackoverflow-lite.herokuapp.com/api/v1/questions'

question_manager = ManageQuestions()
questions = [
    {
        "author": "1",
        "title": "Does my first Mock Test title Work?",
        "body": "Mocking second Test body Text",
        "created_at": str(datetime.now()),
        "id": "1",
        "tags": "html, test, python",
    },
    {
        "author": "1",
        'title': 'Second Mock Test title seems not Working',
        'body': 'Mocking second Test body Text',
        "created_at": str(datetime.now()),
        "id": "2",
        "tags": "html, test, python",
    }
]
question_manager.questions = questions

class TestApi(unittest.TestCase):

    def setUp(self):
        self.questions = question_manager.questions

    def test_get_all_question(self):
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_question(self):
        test_data = {
            "author": "1",
            "title": get_sentence(start_with_lorem=True),
            "body": get_sentence(start_with_lorem=True),
            "tags": "Test, Python"
        }
        response = requests.post(BASE_URL, json= test_data)
        #On successfull Posting, Return success must Equal 1
        self.assertEqual(response.status_code, 201)
    
    def test_get_specific_question(self):
        response = requests.get("{}/1".format(BASE_URL))
        self.assertEqual(response.status_code, 200)
    
    def test_get_specific_question_not_found(self):
        response = requests.get("{}/14r451".format(BASE_URL))
        self.assertEqual(response.status_code, 404)

    def test_successful_delete_question(self):
        response = requests.delete("{}/2".format(BASE_URL))
        self.assertEqual(response.status_code, 200)

    def test_delete_question_not_found(self):
        response = requests.delete('{}/a701'.format(BASE_URL), data=json.dumps({ "author": "2"}) )
        self.assertEqual(response.status_code, 404)

    def test_unauthorised_delete_question(self):
        response = requests.delete('{}/1'.format(BASE_URL), json={"author": "5"})
        self.assertEqual(response.status_code, 401)
 
    def test_post_answer(self):
        test_data = {
            "author": "12",
            "answer": get_sentence(start_with_lorem=True),
        }
        response = requests.post('{}/1/answers'.format(BASE_URL), 
                                json= test_data )
        return self.assertEqual(200, response.status_code)

    def teardown(self):
        # teardown here..for resetting questions
        question_manager.questions = self.questions

if __name__ == '__main__':
    unittest.main()