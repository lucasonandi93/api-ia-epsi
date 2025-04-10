from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from model_accident_utils import lire_fichier_csv, convert_annee, convert_grav

def train_model():
    data_usagers = lire_fichier_csv("data/usagers-2023.csv")
    data_usagers = [d for d in data_usagers if len(d) > 8]

    xy = [
        [convert_annee(d[8]), convert_grav(d[6])]
        for d in data_usagers
    ]
    xy = [d for d in xy if d[0] > -1 and d[1] > -1]

    x_annee = [[d[0]] for d in xy]
    y_gravite = [d[1] for d in xy]

    x_train, _, y_train, _ = train_test_split(
        x_annee, y_gravite, test_size=0.3, random_state=42
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)

    model = LinearRegression()
    model.fit(x_train_scaled, y_train)

    return model, scaler

model, scaler = train_model()

def predict_gravite(annee):
    x = scaler.transform([[annee]])
    return model.predict(x)[0]
