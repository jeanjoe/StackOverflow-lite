<a href="https://codeclimate.com/github/jeanjoe/StackOverflow-lite/maintainability"><img src="https://api.codeclimate.com/v1/badges/f58c45cf7842e94db189/maintainability" /></a>

# StackOverflow-lite
StackOverflow-lite is a platform where people can ask questions and provide answers.

##### Page Link
A preview of the UI Template can be found on [Github Pages](https://jeanjoe.github.io/StackOverflow-lite/)
##### Pivotal Tracker 
Link to [Pivotal Tracker Board](https://www.pivotaltracker.com/projects/2190229)

##### Link to API Endpoint
[BASE URL TO API ENDPOINT](https://manzede-stackoverflow-lite.herokuapp.com/)

## How to Use the Endpoint

##### GET ALL QUESTIONS
Link https://manzede-stackoverflow-lite.herokuapp.com/api/v1/questions

Method: GET

Parameters: NONE

##### POST QUESTION

Link: https://manzede-stackoverflow-lite.herokuapp.com/api/v1/questions

METHOD: POST

PARAMETERS: author(required), title(required), body(required), tags(required)

##### GET SPECIFIC QUESTION

LINK: https://manzede-stackoverflow-lite.herokuapp.com/api/v1/questions/question_ID

METHOD: GET

PARAMETERS: question_ID (required)

##### DELETE QUESTION

LINK: https://manzede-stackoverflow-lite.herokuapp.com/api/v1/questions/question_ID

METHOD: DELETE

PARAMETERS: question_ID

##### POST ANSWER TO A QUESTION

LINK: https://manzede-stackoverflow-lite.herokuapp.com/api/v1/questions/question_ID/answers

METHOD: POST

PARAMETERS: question_ID, autho(required), answer (required)