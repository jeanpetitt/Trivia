from hashlib import new
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
        
        if len(list_cat) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
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
        
        # obtenir une liste de categorie
        categories = Category.query.all()
        list_cat = [categorie.format() for categorie in categories]
        
        # obtenir un nomre de page variable en fonction de la pagination
        # par 10 question
        nb_page = (len(questions) / 10)
        if isinstance(nb_page, int):
            return nb_page
        else:
            nb_page = int(nb_page) + 1
        print(nb_page)

        
        if len(current_questions) == 0:
            abort(404)
            
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': None,
            'nbre_page': nb_page,
            'categories': list_cat,
        })

    # route permettant de supprimer une question
    @app.route("/questions/<int:question_id>/delete", methods=['DELETE'])
    def delete_question(question_id):
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
                    "questions": current_questions, 
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)
    
    # poster une nouvelle question
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_categorie = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        try:
            # rendre l'envoi des donnees au format json obligatoire
            # comme avec un formulaire. tout simplement on ne peut pas
            # envoyer les donnees si au lieu de {'question': 'ma question'} on met
            # {'ques':'ma question'} ou {'question': ''}
            if ((new_question == None or new_question == '') or 
                (new_answer == None or new_answer == '') or 
                (new_categorie == None or new_categorie == '') or 
                (new_difficulty == None or new_difficulty == '')):
                abort(422)
                
            question = Question(question=new_question, answer=new_answer, 
                                category=new_categorie, difficulty=new_difficulty)
            question.insert()
            select = Question.query.order_by(Question.id).all()
            current_questions = paginate_question(request, select)
            
            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'current_category': None
            })
        except:
            abort(422)

    # chercher une question
    # affiche toutes les questions dont le titre correpond au terme entrer par le user
    @app.route('/questions/search', methods=['POST'])
    def search_question(): 
        body = request.get_json()
        question = body.get("search", None)
        
        if question == None or question == '':
                abort(422)
        try:
            # filtrer toutes les questions dont les titres correpondent
            # au terme rechercher de maniere a ce que cela soit non sensible a la casse
            result = Question.query.filter(Question.question.ilike(f'%{question}%')).order_by(Question.id).all()
            
            # paginer le resultat des questions trouves
            current_questions = paginate_question(request, result)
            
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(result),
                'current_question': None,
            })
        except:
            abort(404)
    
    # question permetant d'afficher toutes les question d'une  categorie
    @app.route('/categories/<int:category_id>/questions')    
    def get_question_by_category(category_id):
        try:
            questions = Question.query.filter(Question.category == str(category_id)).order_by(Question.id).all()
            current_questions = paginate_question(request, questions)
            current_category = Category.query.filter(Category.id == category_id)
            
            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': category_id,
                #current_category.type,
                'total_questions': len(current_questions)
            })
        except:
            abort(404)
            
    # mise en place du jeu proprement dit     
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        try:
            body = request.get_json()
            # if not ('quiz_category' in body and 'previous_questions' in body):
            #     abort(422)

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if category['type'] == 'click':
                _questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
        
            # creer une liste de question de tel sorte que l'id des questions
            # precedente ne se retrouve pas a l'interieur
                _questions = Question.query.filter_by(
                    category=category['id']).filter(Question.id.notin_((previous_questions))).all()

            # dans la liste des question creer choisir aleartoirement un question
            new_question = _questions[random.randrange(
                0, len(_questions))].format() if len(_questions) > 0 else None

            print(category)
            print(previous_questions)
            
            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)


    # personnalisation des ereurs 404 et  422
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "ressource Not found"
        }), 404
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422

    return app

