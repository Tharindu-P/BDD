import json
import redis
# Connexion à Redis
redis_client = redis.Redis(host='localhost', port=6380, db=0)

piloteFile = open("PILOTES.txt", 'r', encoding='utf-8')
pilotes = {}

for line in piloteFile:
    line = line.split('\t')
    pilotes[line[0]] = {"id": line[0], "nom": line[1], "naissance": line[2], "ville": line[3].rstrip()}

clientFile = open("CLIENTS.txt", 'r', encoding='utf-8')
clients = {}

for line in clientFile:
    line = line.split('\t')
    clients[line[0]] = {"id": line[0], "nom": line[1], "numeroRue": line[2], "nomRue": line[3], "codePostal": line[4], "ville": line[5].rstrip()}

classesFile = open('DEFCLASSES.txt', 'r', encoding="utf-8")
classes = {}

for line in classesFile:
    line = line.split('\t')
    if line[0] not in classes:
        classes[line[0]] = {line[1]: int(line[2].rstrip())}
    else:
        classes[line[0]][line[1]] = int(line[2].rstrip())

avionsFile = open("AVIONS.txt", 'r', encoding='utf-8')
avions = {}

for line in avionsFile:
    line = line.rstrip().split("\t")
    avions[line[0]] = {"id": line[0], "nom": line[1], "capacite": line[2], "ville": line[3]}

volsFile = open('VOLS.txt', 'r', encoding="utf-8")
vols = {}

for line in volsFile:
    line = line.split("\t")
    vols[line[0]] = {"id": line[0], "villeDepart": line[1], "villeArrivee": line[2], "dateDepart": line[3],
                     "heureDepart": line[4], "dateArrivee": line[5], "heureArrivee": line[6],
                     "pilote": pilotes[line[7]], "avion": avions[line[8].rstrip()]}

reservationFile = open("RESERVATIONS.txt", 'r', encoding='utf-8')
reservations = []

for line in reservationFile:
    line = line.split('\t')
    reservations.append({"id": line[0] + "_" + line[1], "client": clients[line[0]],
                         "vol": vols[line[1]], "classe": {"nom": line[2], "coeffPrix": classes[line[1]][line[2]]}, "places": int(line[3].rstrip())})

for i in range(len(reservations)):
    redis_client.set(f"reservations:{i+1}", json.dumps(reservations[i]))

json.dump(reservations[0], open("testRes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
