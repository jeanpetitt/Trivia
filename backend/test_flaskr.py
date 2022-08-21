import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres','2002','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'question':'who is the president of cameroon', 
            'answer':'Paul Bya',
            'category': '5',
            'difficulty': '5' 
            }
        self.search = {
            'search': 'who'
        }
        self.play_quizz ={
            'previous_questions': [5, 9,  13],
            'quiz_category': {'type': 'click', 'id': 0},
        }
        self.data_play_error = {
            'previous_questions': '',
            'quiz_category': {'type': 'click', 'id': 0},
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    # test qui liste toutes les categories
    def test_get_categories(self):
        _test = self.client().get('/categories')
        data = json.loads(_test.data)
        
        # verification du success
        self.assertEqual(_test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    # erreur si le chemin par lequel on souhaite acceder a la liste des categorie
    # ne correspond pas a celui defini
    def test_404_if_url_get_categorie_not_found(self):
        _test = self.client().get("/categorie")
        data = json.loads(_test.data)

        self.assertEqual(_test.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "ressource Not found")

    # test de pagination des questions
    def test_retrieve_question(self):
        _test = self.client().get('/questions')
        data = json.loads(_test.data)
        
        # verification du succes
        self.assertEqual(_test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        
    # erreur si le chemin par lequel on souhaite acceder a la liste pagines de question
    # ne correspond pas a celui defini ou si le numero de page indique n'existe pas
    def test_404_sent_requesting_beyond_valid_page(self):
        _test = self.client().get("/questions?page=200")
        data = json.loads(_test.data)

        self.assertEqual(_test.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "ressource Not found")
        
    # test de suppression d'une question
    # def test_delete_question(self):
    #     print('************************************************')
    #     print('Delete test:')
    #     print('\t\t before delete: total_question=' ,len(Question.query.all()))
    #     _test = self.client().delete("/questions/15/delete")
    #     data = json.loads(_test.data)
    #     # obtenir l'id de la question a supprimer
    #     question = Question.query.filter(Question.id == 15).one_or_none()
    
    #     # verifier le succes de la suppresion de la question
    #     self.assertEqual(_test.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 15)
    #     self.assertTrue(data["questions"])
    #     self.assertTrue(data["total_questions"])
    #     self.assertEqual(question, None)
    #     print('\t\t after delete: total_question=', data['total_questions'])
    #     print('*************************************************')
    
    # test de suppression echoue(error) si l'id de la question est introuvable
    def test_422_if_id_question_does_not_exist(self):
        _test = self.client().delete("/questions/10000/delete")
        data = json.loads(_test.data)
        self.assertEqual(_test.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # test de creation d'une nouvelle question
    # def test_create_new_question(self):
    #     # optenir le nombre de question avant ajout
    #     print('************************************************')
    #     print('Create_question test:')
    #     print('\t\t before add: total_question=' ,len(Question.query.all()))
    #     _test = self.client().post("/questions", json=self.new_question)
    #     data = json.loads(_test.data)

    #     self.assertEqual(_test.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["created"])
    #     self.assertTrue(data["questions"]) 
    #     self.assertTrue(data["total_questions"])
    #     self.assertEqual(data["current_category"], None)  
    #     print('\t\t after add: total_question=', data['total_questions'])
    #     print('*************************************************') 
    
    # erreur si le chemin qu'on tente d'acceder pour envoyer les donnees ne correspond 
    # a celui defini 
    def test_404_if_url_question_creation_not_found(self):
        _test = self.client().post("/question/30", json=self.new_question)
        data = json.loads(_test.data)

        self.assertEqual(_test.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "ressource Not found")
    
    # test de recherche d'une question
    def test_search_question(self):
        res = self.client().post('/questions/search', json=self.search)
        data = json.loads(res.data)

        # verification du succes du test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["questions"])
    
    # erreur si l'url par lequel on souhaite envoyer
    # le terme de recherche ne correspond a celui definie
    def test_404_if_url_question_search_not_found(self):
        _test = self.client().post("/question/30", json=self.new_question)
        data = json.loads(_test.data)

        self.assertEqual(_test.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "ressource Not found")
    
    # test de question par categorie
    def test_get_question_by_category(self):
        _test = self.client().get("/categories/6/questions")
        data = json.loads(_test.data)       
                
        # verification du succes
        self.assertEqual(_test.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["current_category"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
    
    # erreur si l'url par lequel on souhaite acceder au question d'une category
    # est incorrecte
    def test_404_if_url_category_does_not_exist(self):
        _test = self.client().get("/categorie/1000/questions")
        data = json.loads(_test.data)
        self.assertEqual(_test.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "ressource Not found")   
    
    # test de mise en place du jeu
    def test_play_quizz_game(self):
        _test = self.client().post('/quizzes', json=self.play_quizz)
        data = json.loads(_test.data)
         
        #  verification du succes du test
        self.assertEqual(_test.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    # erreur 422 si le format de donne envoyer est invalide
    def test_422_if_data_play_game_are_not_valid(self):
        _test = self.client().post("/quizzes", json=self.data_play_error)
        data = json.loads(_test.data)
        self.assertEqual(_test.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()