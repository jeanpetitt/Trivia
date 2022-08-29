# Trivia API
  - Trivia est un jeux de Question et Reponse. il permet au joueur de s'instruire avant
  de commencer à jouer au jeu; en les offrant une liste de questions avec reponse dont ils pourront essayer de les memoriser et d'applquer ce qu'ils auront appris. Il offre egalement la possibilite d'ajouter une question avec une reponse a la question, la categorie a laquelle la question ainsi que le degre de difficulter
  `NB: les reponses founient lors du deroulement du jeu sont sensible a la casse c'est a dire que si une reponse contient une Majuscule, a la place vous mettez une minuscule; la reponse sera incorrecte` 

### Pre-requis Developement local
Les développeurs utilisant ce projet doivent déjà avoir Python3, pip et node installés sur leurs machines locales.
sinon consultez 
> [Telecharger la derniere version de python ](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) 
> [Telecharger node](https://nodejs.org/en/download)

# A propos des Stack
`backend`
`fontend`

#### Backend
Naviguez dans le dossier ` backend` et executer
```pip3 intall -r requirements.txt```
tous les packages requis sont inclus dans le fichier requirements.txt.
pour lancer cette application executer les commandes suivant:
  - pour les utilisateurs windows:
```
  set FLASK_APP=flaskr
  set FLASK_ENV=development
  flask run
```
  - pour les utilisateur linux:
```  
  export FLASK_APP=flaskr
  export FLASK_ENV=development
  flask run
```
Ces commandes mettent l'application en développement et ordonnent à notre application d'utiliser le fichier '__init__.py' dans notre dossier flaskr. Travailler en mode développement affiche un débogueur interactif dans la console et redémarre le serveur chaque fois que des modifications sont apportées. L'application est exécutée sur `http://127.0.0.1:5000/` par défaut et est un proxy dans la configuration frontend.

Une fois l'applicationn lancer elle vas creer une base de donnee Trivia, il vas falloir la remplir avec les donnees. Pour cela suivez les instructions suivantes:
```
dropdb trivia
createdb trivia
```
ensuite assurez-vous que vous vous trouvez dans le dossier backend dans un terminal et executez:
```
psql < trivia.psql
```
ou 
```
psql < trivia.psql -U postgres -h localhost trivia
```

#### Frontend
Depuis le dossier frontend, executer les commandes suivantes pour lancer le client frontend:
```
npm install // only once to install dependencies
npm start 
```

par defaut, le frontend se lancera sur localhost:3000. 
consultez: 
> [README frontend](./frontend/README.md) pour plus de detail
### Tests
Etant dans le dossier `backend` tapez les commandes suivantes:
```
dropdb trivia_test
createdb trivia_test
```
```
psql bookshelf_test < books.psql
```
or 
```
psql trivia_test < trivia.psql -U postgres -h localhost bookshelf_test
```
```
python test_flaskr.py
```
La première fois que vous exécutez les tests, omettez la commande dropdb.

Tous les tests sont conservés dans ce fichier et doivent être maintenus au fur et à mesure que des mises à jour sont apportées aux fonctionnalités de l'application.

## pour commencer
### Error Handling
Les erreurs sont renvoyées sous forme d'objets JSON au format suivant :
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
L'API renvoie trois types d'erreur lorsque les demandes échouent:
- 400: Bad Request / requete errone
- 404: Resource Not Found / ressource non trouver
- 422: Not Processable / intraitable

### Endpoints / points de terminaison
pour en savoir plus sur les points de teminaison en utilisant ``curl`` cliquer sur [backend README](./backend/README.md)

## Deployement N/A

## Autheur
Jean Petit, etudiant a udacity 
