def lire_fichier_csv(chemin_fichier, skip_header=True):
    data_csv = []
    with open(chemin_fichier, encoding='utf-8') as fic:
        lines = fic.readlines()
        data_csv = [line.strip().split(";") for line in lines]
        if skip_header:
            data_csv = data_csv[1:]
        return data_csv

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
        "1": 1,
        "2": 100,
        "3": 10,
        "4": 5
    }
    return mapping.get(val, -1)
