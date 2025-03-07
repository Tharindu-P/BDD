import pymongo
import bson

# Créer un MongoClient et accéder à la base de données spécifique
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['reservations']  # Remplace 'nom_de_ta_base' par le nom de ta base de données

# Création des collections si elles n'existent pas
if "avions" not in db.list_collection_names():
    db.create_collection("avions")
if "clients" not in db.list_collection_names():
    db.create_collection("clients")
if "classes" not in db.list_collection_names():
    db.create_collection("classes")
if "pilotes" not in db.list_collection_names():
    db.create_collection("pilotes")
if "reservations" not in db.list_collection_names():
    db.create_collection("reservations")
if "vols" not in db.list_collection_names():
    db.create_collection("vols")

# Accéder aux collections
avions = db.avions
clients = db.clients
classes = db.classes
pilotes = db.pilotes
reservations = db.reservations
vols = db.vols

# Réinitialisation des collections
avions.delete_many({})
clients.delete_many({})
classes.delete_many({})
pilotes.delete_many({})
reservations.delete_many({})
vols.delete_many({})

# Traitement des fichiers pour les pilotes
piloteFile = open("PILOTES.txt", 'r', encoding='utf-8')
pilotesDict = {}

# Traitement des fichiers pour les classes
classesFile = open('DEFCLASSES.txt', 'r', encoding="utf-8")
classesDict = {}

for line in classesFile:
    line = line.split('\t')
    if line[0] not in classesDict:
        classesDict[line[0]] = {line[1]: int(line[2].rstrip())}
    else:
        classesDict[line[0]][line[1]] = int(line[2].rstrip())

classesDictv2 = {}
for vol in classesDict:
    for clas in classesDict[vol]:
        obj = bson.ObjectId()
        if f"{vol}_{clas}" not in classesDictv2:
            classesDictv2[f"{vol}_{clas}"] = {"_id": obj, "vol": vol, "classe": clas, "coeffPrix": classesDict[vol][clas]}
            classes.insert_one(classesDictv2[f"{vol}_{clas}"])

# Traitement des fichiers pour les pilotes
for line in piloteFile:
    obj = bson.ObjectId()
    line = line.split('\t')
    pilotesDict[line[0]] = {"_id": obj, "nom": line[1], "naissance": line[2], "ville": line[3].rstrip()}
    pilotes.insert_one(pilotesDict[line[0]])

# Traitement des fichiers pour les clients
clientFile = open("CLIENTS.txt", 'r', encoding='utf-8')
clientsDict = {}

for line in clientFile:
    obj = bson.ObjectId()
    line = line.split('\t')
    clientsDict[line[0]] = {"_id": obj, "nom": line[1], "numeroRue": line[2], "nomRue": line[3], "codePostal": line[4], "ville": line[5].rstrip()}
    clients.insert_one(clientsDict[line[0]])

# Traitement des fichiers pour les avions
avionsFile = open("AVIONS.txt", 'r', encoding='utf-8')
avionsDict = {}

for line in avionsFile:
    obj = bson.ObjectId()
    line = line.rstrip().split("\t")
    avionsDict[line[0]] = {"_id": obj, "nom": line[1], "capacite": line[2], "ville": line[3]}
    avions.insert_one(avionsDict[line[0]])

# Traitement des fichiers pour les vols
volsFile = open('VOLS.txt', 'r', encoding="utf-8")
volsDict = {}

for line in volsFile:
    obj = bson.ObjectId()
    line = line.split("\t")
    volsDict[line[0]] = {
        "_id": obj,
        "villeDepart": line[1],
        "villeArrivee": line[2],
        "dateDepart": line[3],
        "heureDepart": line[4],
        "dateArrivee": line[5],
        "heureArrivee": line[6],
        "pilote": pilotesDict[line[7]]["_id"],
        "avion": avionsDict[line[8].rstrip()]["_id"]
    }
    vols.insert_one(volsDict[line[0]])

# Traitement des fichiers pour les réservations
reservationFile = open("RESERVATIONS.txt", 'r', encoding='utf-8')

for line in reservationFile:
    obj = bson.ObjectId()
    line = line.split('\t')
    reservations.insert_one({
        "_id": obj,
        "client": clientsDict[line[0]]["_id"],
        "vol": volsDict[line[1]]["_id"],
        "classe": classesDictv2[f"{line[1]}_{line[2]}"]["_id"],
        "places": int(line[3].rstrip())
    })
