import unittest, json, requests

import api

BASE_URL = 'http://127.0.0.1:5000/api/v1/questions'

question_manager = api.ManageQuestions()

class TestApi(unittest.TestCase):

    def setUp(self):
        self.api = question_manager.questions(question_data)
      

if __name__ == '__main__':
    unittest.main()