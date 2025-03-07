import json
import redis

# Connexion à Redis
client_redis = redis.Redis(host='localhost', port=6380, db=0)

def getPilotes(client_redis, id_pilote=None, nom_pilote=None):
    # Liste pour stocker les informations de vol
    informations_vol = []
    
    # Variables pour stocker les informations du pilote trouvé
    nom_pilote_trouve = None  
    id_pilote_trouve = None  
    date_naissance_pilote_trouve = None  
    ville_pilote_trouve = None  

    # Parcours de toutes les clés de réservation dans Redis
    for cle in client_redis.scan_iter("reservations:*"):
        donnees_reservation = client_redis.get(cle)
        
        if donnees_reservation:
            reservation = json.loads(donnees_reservation)
            informations_pilote = reservation["vol"]["pilote"]

            # Vérifier si on utilise id_pilote ou nom_pilote pour filtrer
            if id_pilote and informations_pilote["id"] == id_pilote:
                informations_vol.append(reservation["vol"])  # Ajoute les informations de vol à la liste
                nom_pilote_trouve = informations_pilote["nom"]  # Récupère le nom du pilote
                id_pilote_trouve = id_pilote  # Récupère l'ID du pilote trouvé
                date_naissance_pilote_trouve = informations_pilote["naissance"]  # Récupère la date de naissance
                ville_pilote_trouve = informations_pilote["ville"]  # Récupère la ville du pilote
            elif nom_pilote and informations_pilote["nom"].lower() == nom_pilote.lower():
                informations_vol.append(reservation["vol"])  # Ajoute les informations de vol à la liste
                nom_pilote_trouve = informations_pilote["nom"]  # Récupère le nom du pilote
                id_pilote_trouve = informations_pilote["id"]  # Récupère l'ID du pilote trouvé
                date_naissance_pilote_trouve = informations_pilote["naissance"]  # Récupère la date de naissance
                ville_pilote_trouve = informations_pilote["ville"]  # Récupère la ville du pilote

    # Utiliser un ensemble pour éviter les doublons dans les informations de vol
    vols_uniques = {vol['id']: vol for vol in informations_vol}.values()

    # Affichage des informations personnelles du pilote
    if nom_pilote_trouve:
        print(f"Informations sur le pilote: {nom_pilote_trouve} (ID: {id_pilote_trouve})")
        print(f"Date de naissance: {date_naissance_pilote_trouve}, Ville: {ville_pilote_trouve}")
    else:
        print("Aucun pilote trouvé avec les informations fournies.")

    # Affichage des résultats des vols
    if vols_uniques:
        for vol in vols_uniques:
            print(f"Numéro de vol: {vol['id']}, "
                  f"Avion: {vol['avion']['nom']}, "
                  f"Ville de départ: {vol['villeDepart']}, "
                  f"Ville d'arrivée: {vol['villeArrivee']}, "
                  f"Date de départ: {vol['dateDepart']}, "
                  f"Heure de départ: {vol['heureDepart']}, "
                  f"Date d'arrivée: {vol['dateArrivee']}, "
                  f"Heure d'arrivée: {vol['heureArrivee']}")
    else:
        print(f"Aucun vol trouvé pour le pilote {nom_pilote_trouve} (ID: {id_pilote_trouve}).")

def obtenir_informations_pilote():
    # Demande à l'utilisateur d'entrer l'ID et le nom du pilote
    id_pilote = input("Veuillez entrer l'ID du pilote (ou autre pour ignorer): ")
    nom_pilote = input("Veuillez entrer le nom du pilote (ou autre pour ignorer): ")

    # Vérification de la validité de l'ID du pilote
    if not id_pilote.isdigit():  # Vérifie si id_pilote est un nombre
        id_pilote = None
    else:
        id_pilote = str(id_pilote)  # Convertit l'ID en chaîne

    # Vérification de la validité du nom du pilote
    if not nom_pilote.strip():  # Vérifie si nom_pilote est vide
        nom_pilote = None
    else:
        nom_pilote = nom_pilote.strip()

    # Appel de la fonction de recherche
    print('------------------------------------------------')
    getPilotes(client_redis, id_pilote, nom_pilote)


obtenir_informations_pilote()
