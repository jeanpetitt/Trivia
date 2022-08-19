import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# fonction qui permet de regrouper 10 questions par page
def paginate_question(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    #headers cors
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTION"
        )
        return response
        
    # route qui affiche la liste de toutes les categories
    @app.route('/categories', methods=['GET'])
    def get_category():
        categories = Category.query.all()
        # obtenir une liste de categorie
        list_cat = [categorie.format() for categorie in categories]
        return jsonify({
            'categories': list_cat,
        })
    
    # chemin qui recupere toutes 10 les questions, par page, 
    # le nombre total des question, la liste des categories courante,
    # la liste de toutes les categories
    @app.route('/questions')
    def retrieve_questions():
        # questions
        select_question = Question.query.order_by(Question.id).all()
        current_questions = paginate_question(request, select_question)
        questions = Question.query.all()
        # categories
        select_category = Category.query.order_by(Category.id).all()
        current_categories = paginate_question(request, select_category)
        categories = Category.query.all()
        
        # obtenir une liste de categorie
        list_cat = [categorie.format() for categorie in categories]
        
        if len(current_questions) == 0:
            abort(404)
            
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': current_categories,
            'categories': list_cat,
        })

    # route permettant dupprimer une question
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_book(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            select = Question.query.order_by(Question.id).all()
            current_questions = paginate_question(request, select)
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "question": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

