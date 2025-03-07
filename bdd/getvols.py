import json
import redis

# Connexion à Redis
client_redis = redis.Redis(host='localhost', port=6380, db=0)

def rechercher_vols(client_redis, numero_vol=None, ville_depart=None, ville_arrivee=None):
    # Liste pour stocker les informations de vol
    informations_vol = []
    vols_deja_vus = set()  
    # Parcours de toutes les clés de réservation dans Redis
    for cle in client_redis.scan_iter("reservations:*"):
        donnees_reservation = client_redis.get(cle)
        
        if donnees_reservation:
            reservation = json.loads(donnees_reservation)
            vol = reservation["vol"]

            # Vérification des critères de recherche
            match = True  # Par défaut, considérer qu'il y a une correspondance

            if numero_vol and vol["id"] != numero_vol:
                match = False  # False si le numéro de vol fourni ne correspond pas

            if ville_depart and vol["villeDepart"].lower() != ville_depart.lower():
                match = False  

            if ville_arrivee and vol["villeArrivee"].lower() != ville_arrivee.lower():
                match = False 

            # Ajouter le vol uniquement s'il correspond à tous les critères et n'a pas déjà été vu
            if match and vol["id"] not in vols_deja_vus:
                informations_vol.append(vol)
                vols_deja_vus.add(vol["id"])  # Ajouter l'ID du vol à l'ensemble

    # Affichage des résultats
    if informations_vol:
        print(f"Résultats de la recherche :")
        for vol in informations_vol:
            print(f"Numéro de vol: {vol['id']}")
            print("Informations sur le vol:")
            print(json.dumps(vol, indent=4))
    else:
        print("Aucun vol trouvé avec les critères spécifiés.")

def obtenir_criteres_recherche():
    numero_vol = input("Veuillez entrer le numéro de vol (ou autre pour ignorer): ")
    ville_depart = input("Veuillez entrer la ville de départ (ou autre pour ignorer): ")
    ville_arrivee = input("Veuillez entrer la ville d'arrivée (ou autre pour ignorer): ")

    # Conversion des entrées si vides
    numero_vol = numero_vol.strip() if numero_vol.strip() else None
    ville_depart = ville_depart.strip() if ville_depart.strip() else None
    ville_arrivee = ville_arrivee.strip() if ville_arrivee.strip() else None

    # Appel de la fonction de recherche avec les valeurs appropriées
    print('------------------------------------------------')
    rechercher_vols(client_redis, numero_vol, ville_depart, ville_arrivee)

obtenir_criteres_recherche()
