# Full Stack API Final Project

This is a project submission for Udacity's Full Stack Web Development Nanodegree. The Project template was provided by Udacity, my main work was in `backend/__init__.py` (the behavior of the API endpoints) and `backend/test_flaskr.py` (tests for these endpoints), and this Readme (adapted from Udacity's instructions). Check out the commit history if you want to evaluate my changes in detail.

The application is a quiz app. It is possible to browse questions from different categories, search for questions by search terms, create and delete questions, and request a 'quiz' based on a specific category which will randomly select a new questions from a given category to be answered by the user.

## Getting Started

This application consists of a backend and frontend, each in their own directories.

### Backend

#### Prerequisites

* Postgres 
* Python 3 ([setup guide](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python))
* Working in a virtual environment is recommended ([setup guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/))

#### Install requirements
With the requirements in place, install the dependencies by running

```bash
pip install -r requirements.txt
```

#### Setup database

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

This app expects a db named `trivia` and postgres running `localhost:5423` (not the default port!), with user `postgres` and pwd `postgres`.

You can change these in `models.py` if your setup is different.

#### Run the app

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

The backend will run locally at http://127.0.0.1:3000/. See below for how to use it through the frontend.

#### Running the tests

The tests run against the db `trivia_test`. 

To initialize:

```
createdb trivia_test
psql trivia_test < trivia.psql
```

And to run the tests:
```
python3 test_flaskr.py
```

It may be necessary to re-initialize the db after tests. To do so, run

```
dropbd trivia_test
```

and start over.

### Frontend

This is a React app which requires an existing installation of [node.js](https://nodejs.org) and [NPM](https://www.npmjs.com/)

With these installed, build the app with

```
npm install
```

and run it with 

```
npm start
```

For any meaningful interaction with this app, the backend has to be running.

The frontend will run locally at http://127.0.0.1:3000/

## API Reference

This describes the backend endpoints.

### Getting Started

Base URL: The backend app runs locally under http://127.0.0.1:5000/  
No authentication is implemented.

### Error Handling

Each successful request will contain the following key in its JSON response:

```
success: True
```

Errors will be returned in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Unprocessable Entity

### Endpoints

#### GET /

General: Returns `status: ok` if server is running.
Sample: Sample: curl http://127.0.0.1:5000/

```
{ 'status':'ok' }
```

#### GET /questions

General:
 * Returns all categories as a dictionary 
 * Returns all questions, paginated in groups of 10.
Sample: `curl http://127.0.0.1:5000/books`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "", 
      "category": 1, 
      "difficulty": 1, 
      "id": 84, 
      "question": ""
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 26
}
```

#### GET /categories

General: Returns all categories as a dictionary.
Sample: `curl http://127.0.0.1/categories`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### GET /categories/<id>/questions

General: 
* Returns the category for the given id
* Returns all questions for that category
Sample: `curl http://127.0.0.1/categories/4/questions`

```
{
  "current_category": {
    "4": "History"
  }, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": null, 
      "id": 24, 
      "question": "Who invented peanut butter?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

#### POST /questions

This serves to search for questions or post new questions.

1. Search questions matching search_term
General:
* if a `searchTerm` is specified in the payload of the POST request, this returns questions found matching that search term. 
* if no match is found, this returns an empty list (rather than an error 404)

Sample: 
```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "searchTerm": "mirrors" }'
```

```
{
  "questions": [
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

2. Create a new question
General:
* if no search_term is provided, this endpoint tries to create a new question based on the payload data.
* a question, answer, category, and difficulty must be specified in the payload.
* if the payload is missing any of that data, a 400 error (bad request) is returned. 
* other errors during processing will result in a 422.
* if question is created successfully, it returns a success message.

Sample:
```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is the answer to the great question?", "answer": "42", "difficulty": "5", "category": "5" }'
```

```
{
  "success": true
}
```

#### DELETE/questions/<id> 

General:
* Deletes the question with the given id
* If no question exists with the given id, returns a 404 error.

Sample: `curl http://127.0.0.1:5000/questions/28 -X DELETE`

```
{
  "success": true
}
```

#### POST /quizzes

General: 
 * Returns a random question, from the category specified in the POST request payload, excluding the previous questions specified in the payload.

Sample: 
```
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [16, 18, 19], "quiz_category": {"type": "Art", "id": "2"}}'
```

```
{
  "question": {
    "answer": "Mona Lisa", 
    "category": 2, 
    "difficulty": 3, 
    "id": 17, 
    "question": "La Giaconda is better known as what?"
  }, 
  "success": true
}

```

## Authors

Sebastian (xbow), based on info provided by Udacity (regarding setup) and patterns presented in the course (API documentation format).

