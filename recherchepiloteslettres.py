import json
import redis

# Connexion à Redis
client_redis = redis.Redis(host='localhost', port=6380, db=0)

def compter_pilotes_par_nom(client_redis, lettre):
    """Compter le nombre de pilotes dont le nom de famille contient une lettre donnée, sans doublons."""
    compteur_pilotes = 0
    noms_de_pilotes = set()  # Utilisation d'un ensemble pour éviter les doublons

    # Parcours de toutes les clés de réservation dans Redis
    for cle in client_redis.scan_iter("reservations:*"):
        donnees_reservation = client_redis.get(cle)
        
        if donnees_reservation:
            reservation = json.loads(donnees_reservation)  # Conversion JSON
            
            # Accéder au nom du pilote
            nom_pilote = reservation["vol"]["pilote"]["nom"]  # Supposons que le nom du pilote est sous cette clé
            
            # Vérifier si la lettre est présente dans le nom du pilote
            if lettre.lower() in nom_pilote.lower():  # Recherche insensible à la casse
                # Si le nom n'a pas encore été compté, l'ajouter à l'ensemble et incrémenter le compteur
                if nom_pilote not in noms_de_pilotes:
                    noms_de_pilotes.add(nom_pilote)  # Ajoute le nom à l'ensemble
                    compteur_pilotes += 1  # Incrémente le compteur si c'est un nouveau pilote

    print(f"Nombre de pilotes dont le nom de famille contient la lettre '{lettre}': {compteur_pilotes}")

# Exemple d'utilisation de la fonction
lettre_recherche = input("Veuillez entrer une lettre pour rechercher les pilotes: ")
compter_pilotes_par_nom(client_redis, lettre_recherche)
