from apiflask import APIFlask, Schema
from apiflask.fields import Integer, String
from flask_sqlalchemy import SQLAlchemy
from modele import predict_gravite

app = APIFlask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accidents.db'
db = SQLAlchemy(app)

# === Base de données ===
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    annee = db.Column(db.Integer, nullable=False)
    gravite = db.Column(db.Integer, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)

# === Schemas ===
class AnneeInput(Schema):
    annee = Integer(required=True)

class GraviteOutput(Schema):
    gravite = Integer()
    categorie = String()

# === Interprete le score en catégorie lisible ===
def interpret_gravite(val):
    if val >= 80:
        return "Tué"
    elif val >= 8:
        return "Blessé hospitalisé"
    elif val >= 3:
        return "Blessé léger"
    elif val >= 0:
        return "Indemne"
    return "Inconnu"

# === Endpoint de prédiction ===
@app.post('/predict')
@app.input(AnneeInput)
@app.output(GraviteOutput)
def predict(json_data):
    annee = json_data['annee']
    gravite = float(predict_gravite(annee))
    categorie = interpret_gravite(gravite)

    print(f"[PREDICTION] Année: {annee} → Gravité: {gravite:.2f} → Catégorie: {categorie}")

    pred = Prediction(annee=annee, gravite=int(round(gravite)), categorie=categorie)
    db.session.add(pred)
    db.session.commit()

    return {
        'gravite': round(gravite),
        'categorie': categorie
    }

# === Endpoint de consultation ===
@app.get('/predictions')
def all_predictions():
    results = Prediction.query.all()
    return [
        {'annee': r.annee, 'gravite': r.gravite, 'categorie': r.categorie}
        for r in results
    ]

# === Lancement ===
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run("0.0.0.0", 9090, debug=True)
