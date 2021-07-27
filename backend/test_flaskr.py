import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
  '''This class represents the trivia test case'''

  def setUp(self):
    '''Define test variables and initialize app.'''
    self.app = create_app()
    self.client = self.app.test_client

    database_name = "trivia_test"
    user = "postgres"
    pwd = "postgres"
    self.database_path = "postgresql://{}:{}@{}/{}".format(user, pwd, 'localhost:5423', database_name)
    setup_db(self.app, self.database_path)

    # as in the library tutorial, prepare a new record to use for testing
    self.new_question = {
        'question': 'What is the answer to the great question?',
        'answer': '42',
        'difficulty': 3,
        'category': 1
    }

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      self.db.create_all()

  def tearDown(self):
    '''Executed after reach test'''
    pass

  # Note: assertions are based on the data in trivia.psql. See readme on how to
  # reset the trivia_test DB if it doesn't match the assertions.

  def test_get_categories(self):
    '''It returns the categories'''

    expectedCategories = {
      '1': 'Science',
      '2': 'Art',
      '3': 'Geography',
      '4': 'History',
      '5': 'Entertainment',
      '6': 'Sports'
    }

    response = self.client().get('/categories')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['categories'], expectedCategories)

    pass

  def test_get_questions_by_category(self):
    '''It retrieves questions by category'''

    response = self.client().get('/categories/3/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['total_questions'], 3)
    self.assertEqual(len(data['questions']), 3)
    self.assertEqual(data['current_category'], { '3': 'Geography'})

    pass


  def test_get_questions_by_category(self):
    '''When no questions exist for a category, it returns 404'''

    # this category will be available for the test, but isn't persisted so it
    # will not affect other tests
    empty_category = Category(type = 'dummy')

    response = self.client().get('/categories/{}/questions'.format(empty_category.id))
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)

    pass

  def test_422_get_question_by_nonexisting_category(self):
    '''When requesting questions for non-existing category, it returns 422'''

    response = self.client().get('/categories/9/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 422)

    pass

  def test_get_questions(self):
    '''It gets questions'''

    expected_total = Question.query.count()

    response = self.client().get('/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['total_questions'], expected_total)
    self.assertEqual(len(data['questions']), 10)

    pass

  def test_delete_question(self):
    '''It deletes a question'''

    initialCount = Question.query.count()

    question = Question(
      answer = 'dummy answer',
      category = 2,
      difficulty = 1,
      question = 'dummy question'
    )
    question.insert()    

    response = self.client().delete('questions/{}'.format(question.id))
    data = json.loads(response.data)
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(Question.query.count(), initialCount)

    pass

  def test_404_when_deleting_nonexisting_question(self):
    '''On a delete request for a non-existing question, it returns 404'''

    initialCount = Question.query.count()

    response = self.client().delete('questions/1')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertEqual(Question.query.count(), initialCount)

    pass

  def test_create_question(self):
    '''It creates a question'''

    initialCount = Question.query.count()

    response = self.client().post('/questions', json=self.new_question)
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)

    newCount = Question.query.count()
    self.assertEqual(newCount, initialCount + 1)

    new_question = Question.query.filter(Question.answer=='42').first()
    self.assertEqual(new_question.question, 'What is the answer to the great question?')

    pass
  
  def test_400_for_bad_post_request(self):
    '''It returns 400 when posting an invalid request to /questions'''

    initialCount = Question.query.count()

    response = self.client().post('/questions', json={ 'foo': 'bar' })
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 400)
    
    newCount = Question.query.count()
    self.assertEqual(newCount, initialCount)

    pass

  def test_get_question_by_search_term(self):
    '''It finds questions matching a search term'''

    response = self.client().post('/questions', json={ 'searchTerm': 'Who' })
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['total_questions'], 3)
    self.assertEqual(len(data['questions']), 3)
    
    pass

  def test_get_question_by_search_term_no_match(self):
    '''When no questions match the search term, it returns an empty list'''

    response = self.client().post('/questions', json={ 'searchTerm': 'Asdfghj' })
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['total_questions'], 0)
    self.assertEqual(len(data['questions']), 0)
    
    pass

  def test_get_quiz_for_category(self):
    '''It retrieves a quiz'''

    payload = {
      'previous_questions': [16, 18, 19],
      'quiz_category': {'type': 'Art', 'id': '2'}
    }

    response = self.client().post('/quizzes', json=payload)

    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)

    # it returns the only question in the category not included in previous_questions
    self.assertEqual(data['question']['id'], 17)

    pass

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()