import json
import redis

# Connexion à Redis
client_redis = redis.Redis(host='localhost', port=6380, db=0)

def getClient(client_redis, id_client=None, nom_client=None):
    # Initialisation des variables pour stocker les informations
    nombre_reservations = 0
    total_places = 0  # Total des places réservées
    informations_vol = []  # Liste pour stocker les informations de vol
    nom_client_trouve = None
    id_client_trouve = None
    adresse_client_trouve = None 

    # Parcours de toutes les clés de réservation dans Redis
    for cle in client_redis.scan_iter("reservations:*"):
        donnees_reservation = client_redis.get(cle)
        
        if donnees_reservation:
            reservation = json.loads(donnees_reservation)  # Conversion JSON

            # Vérifier si on utilise id_client ou nom_client pour filtrer
            if (id_client and reservation["client"]["id"] == id_client) or \
               (nom_client and reservation["client"]["nom"].lower() == nom_client.lower()):
                # Incrémentation des compteurs et stockage des informations
                nombre_reservations += 1
                total_places += reservation["places"]
                
                # Ajout des informations de vol avec le nombre de places réservées
                informations_vol.append({
                    **reservation["vol"],  # Copie les informations de vol
                    "places_reservees": reservation["places"]  # Ajoute le nombre de places réservées
                })

                # Stockage des informations sur le client
                nom_client_trouve = reservation["client"]["nom"]  # Nom du client
                id_client_trouve = reservation["client"]["id"] if not id_client else id_client  # ID du client
                adresse_client_trouve = f"{reservation['client']['numeroRue']} {reservation['client']['nomRue']}, " \
                                        f"{reservation['client']['codePostal']} {reservation['client']['ville']}"  # Adresse

    # Affichage des informations personnelles du client
    if nom_client_trouve:
        print(f"Informations sur le client: {nom_client_trouve} (ID: {id_client_trouve})")
        print(f"Adresse: {adresse_client_trouve}")
    else:
        print(f"Aucun client trouvé avec les informations fournies.")

    # Affichage des résultats
    if nombre_reservations > 0:
        print(f"Nombre de réservations pour le client {nom_client_trouve} (ID: {id_client_trouve}): {nombre_reservations}")
        print(f"Total des places réservées: {total_places}")
        for vol in informations_vol:
            print(f"Numéro de vol: {vol['id']}")
            print("Informations sur le vol:")
            print(json.dumps(vol, indent=4))
def obtenir_informations_client():
    # Demande à l'utilisateur de saisir l'ID et le nom du client
    id_client = input("Veuillez entrer l'ID du client (ou autre pour ignorer): ")
    nom_client = input("Veuillez entrer le nom du client (ou autre pour ignorer): ")

    # Vérification de la validité de l'ID du client
    id_client = str(id_client) if id_client.isdigit() else None

    # Vérification de la validité du nom du client
    nom_client = nom_client.strip() if nom_client.strip() else None

    # Appel de la fonction de recherche avec les valeurs appropriées
    print('------------------------------------------------')
    getClient(client_redis, id_client, nom_client)

# Exécution de la fonction pour obtenir les informations du client
obtenir_informations_client()
