from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

import matplotlib
matplotlib.use('Agg')  # 👉 fuerza matplotlib a usar un backend sin interfaz gráfica
import matplotlib.pyplot as plt

# === Lecture des fichiers CSV ===
def lire_fichier_csv(chemin_fichier, skip_header=True):
    data_csv = []
    with open(chemin_fichier, encoding='utf-8') as fic:
        lines = fic.readlines()
        data_csv = [line.strip().split(";") for line in lines]
        if skip_header:
            data_csv = data_csv[1:]
        return data_csv

data_usagers = lire_fichier_csv("data/usagers-2023.csv")

# === Conversion et nettoyage des champs ===
def convert_annee(val):
    val = val.strip().replace('"', '').replace(' ', '')
    try:
        annee = int(val)
        if 1900 <= annee <= 2025:
            return annee
    except:
        pass
    return -1

def convert_grav(val):
    val = val.strip().replace('"', '').replace(' ', '')
    mapping = {
        "1": 1,    # Indemne
        "2": 100,  # Tué
        "3": 10,   # Blessé hospitalisé
        "4": 5     # Blessé léger
    }
    return mapping.get(val, -1)

# Filtrage et conversion
data_usagers = [d for d in data_usagers if len(d) > 8]

print("Exemples de conversion :")
for d in data_usagers[:5]:
    print(f"Année: {d[8]} -> {convert_annee(d[8])}, Gravité: {d[6]} -> {convert_grav(d[6])}")

xy = [
    [convert_annee(d[8]), convert_grav(d[6])]
    for d in data_usagers
]

xy = [d for d in xy if d[0] > -1 and d[1] > -1]

x_annee = [[d[0]] for d in xy]  # 2D pour sklearn
y_gravite = [d[1] for d in xy]

print("Taille des données en entrée :", len(data_usagers), "retenus :", len(x_annee), len(y_gravite))

# === Split et normalisation
x_train, x_test, y_train, y_test = train_test_split(
    x_annee, y_gravite, test_size=0.3, random_state=42
)

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# === Modèle
model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

# === Graphique
plt.figure(figsize=(10, 6))
plt.scatter(x_test, y_test, alpha=0.3, label="Réel")
plt.scatter(x_test, y_pred, color='red', alpha=0.3, label="Prédit")
plt.xlabel("Année de naissance (standardisée)")
plt.ylabel("Gravité")
plt.title("Prédiction de la gravité selon l'année de naissance")
plt.legend()
plt.grid(True)

# 💾 Sauvegarde du graphique
plt.savefig("resultat_modele.png")
print("✅ Graphique sauvegardé dans 'resultat_modele.png'")
