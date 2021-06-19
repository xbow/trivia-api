import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  

  # Cors
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  # Utils

  def get_categories_dict():
    query = Category.query.all()
    return {category.id: category.type for category in query}

  # Note to reviewer: To keep my route handlers tidy, I refactored some functionality
  # into separate methods here, but it seems a bit weird to have them up here on top
  # of this file. Any advice on best practices for better organizing such code in
  # flask/pyhton is appreciated.

  def create_question(payload):
    question = Question(
      answer = payload.get('answer'),
      category = payload.get('category'),
      difficulty = payload.get('difficutly'),
      question = payload.get('question')
    )

    question.insert()    
      
    return jsonify({
      'success': True
    }), 200

  def find_questions(term):
    results = Question.query.filter(Question.question.ilike(f'%{term}%')).all()

    # If nothing is found, an empty list is returned.
    # Aborting with a 404 code would result in an alert message in frontend, 
    # falsely suggesting there was an error with processing the request.

    questions = [question.format() for question in results]

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(questions),
      'current_category': None
      })


  # Routes

  @app.route('/')
  def hello_world():
    return jsonify({'message':'HELLO, WORLD!'})


  @app.route('/categories')
  def get_categories():

    categories = get_categories_dict()

    return jsonify({
      'success': True,
      'categories': categories
      })


  @app.route('/questions')
  def get_questions():

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions_query = Question.query.all()
    questions = [question.format() for question in questions_query]

    categories = get_categories_dict()

    return jsonify({
      'success': True,
      'questions': questions[start:end],
      'categories': categories,
      'total_questions': len(questions),
      'current_category': None
      })


  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions_query = Question.query.filter_by(category=category_id)
    questions = [question.format() for question in questions_query]

    category_query = Category.query.filter_by(id=category_id).one_or_none()
    category = { category_query.id: category_query.type }

    return jsonify({
      'success': True,
      'questions': questions[start:end],
      'total_questions': len(questions),
      'current_category': category
      })


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()
    
    if question is None:
      abort(404)

    question.delete()

    return jsonify({
      'success': True
    }), 200


  @app.route('/questions', methods=['POST'])
  def post_question():

    payload = request.get_json()

    if payload.get('searchTerm'):
      return find_questions(payload.get('searchTerm'))

    else: 
      return create_question(payload)

  @app.route('/quizzes', methods=['POST'])
  def get_random_question():

    payload = request.get_json()

    category_id = payload.get('quiz_category')['id']
    previous_questions = payload.get('previous_questions')

    all_questions = []
    if (category_id == 0):
      all_questions = Question.query.all() 
    else:
      all_questions = Question.query.filter_by(category = category_id).all()
      
    unanswered_questions = [question for question in all_questions if question.id not in previous_questions]

    if (len(unanswered_questions) < 1):
      abort(404)

    random_index = random.randrange(0, len(unanswered_questions), 1)
    random_question = unanswered_questions[random_index]

    return jsonify({
      'success': True,
      'question': random_question.format()
    })    

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    