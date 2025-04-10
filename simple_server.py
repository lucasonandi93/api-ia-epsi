# from flask import Flask

from apiflask import APIFlask, Schema
from apiflask.fields import String


class Personne(Schema):
    nom = String(required=True)
    prenom = String(required=False)


class Identifiant(Schema):
    identifiant = String()

app = APIFlask("Mon serveur Flask")

@app.get('/personne/<string:nom>')
@app.output(Identifiant)
def get_identifiant(nom):
    return { "identifiant": nom  + "_007"}

@app.post('/personne')
@app.input(Personne(partial=False))
@app.output(Identifiant)
@app.doc(description="Récupère l'identifiant d'une personne à partir de son nom et prénom",
         responses={200: 'Identifiant généré avec succès',
                    202: 'Une autre personne a déjà le même nom',
                    400: 'Erreur de validation des données',
                    500: 'Erreur interne du serveur'})
def get_post_personne(json_data):
    p= Personne()
    p.nom = json_data["nom"]
    p.prenom = json_data["prenom"]

    return { "identifiant": p.nom  +"_"+ p.prenom +"_007"}

# app = Flask("Mon serveur Flask")

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/json')
def hello_world_json():
    return { "message": "<p>Hello, World!</p>" }

# flask app simple_server run
app.run("0.0.0.0", 9090, True, True)