import redis
import json

# Connexion à Redis
redis_client = redis.Redis(host='localhost', port=6380, db=0)

# Ensemble pour stocker les villes de départ et d'arrivée
villes_depart = set()
villes_arrivee = set()

# Parcours des clés de réservations stockées dans Redis
for i in range(1, 100):  # Supposons qu'il y a moins de 100 réservations
    reservation_key = f"reservations:{i}"
    
    # Vérification si la clé existe dans Redis
    if redis_client.exists(reservation_key):
        # Récupérer la réservation en JSON et la charger en dict Python
        reservation_data = json.loads(redis_client.get(reservation_key))
        
        # Ajouter les villes de départ et d'arrivée aux ensembles correspondants
        villes_depart.add(reservation_data['vol']['villeDepart'])
        villes_arrivee.add(reservation_data['vol']['villeArrivee'])
    else:
        # Si aucune clé supplémentaire n'existe, on peut arrêter la boucle
        break

# Affichage des résultats
print("Villes de départ:", villes_depart)
print("Villes d'arrivée:", villes_arrivee)
