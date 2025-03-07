import pymongo

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['reservations']

def get_pilotes():
    pilotes = set()  # Utilisation d'un ensemble pour éviter les doublons

    # Parcours des réservations dans la collection
    for reservation in db.reservations.find():
        # Récupérer le document de vol associé
        vol = db.vols.find_one({"_id": reservation["vol"]})  # Cherche le vol par son ObjectId
        
        if vol and "pilote" in vol:
            # Cherche le pilote associé au vol
            pilote = db.pilotes.find_one({"_id": vol["pilote"]})
            
            if pilote and "nom" in pilote:
                pilotes.add(pilote["nom"])  # Ajoute le nom du pilote à l'ensemble

    nombre_pilotes = len(pilotes)
    
    return pilotes, nombre_pilotes

# Appel de la fonction et affichage des résultats
pilotes_trouves, nombre_total = get_pilotes()
print("Noms des pilotes :", pilotes_trouves)
print("Nombre total de pilotes :", nombre_total)
