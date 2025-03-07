import redis
import json

# Connexion à Redis
redis_client = redis.Redis(host='localhost', port=6380, db=0)

def get_NBpilotes():
    pilotes = set()  # Utilisation d'un ensemble pour éviter les doublons

    # Parcours de toutes les clés correspondant au modèle "reservations:*"
    for reservation_key in redis_client.scan_iter("reservations:*"):
        # Récupérer la réservation en JSON et la charger
        reservation_data = json.loads(redis_client.get(reservation_key))
        # Accéder au nom du pilote dans les informations de vol
        pilotes.add(reservation_data['vol']['pilote']['nom'])

    nombre_total_pilotes = len(pilotes)
    
    return pilotes, nombre_total_pilotes

# Appel de la fonction et affichage des résultats
pilotes_trouves, nombre_total = get_NBpilotes()
print("Noms des pilotes :", pilotes_trouves)
print("Nombre total de pilotes :", nombre_total)
