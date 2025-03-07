import json
import redis

# Connexion à Redis
redis_client = redis.Redis(host='localhost', port=6380, db=0)

def fetch_reservations():
    """Récupère toutes les réservations."""
    reservations = []
    for key in redis_client.scan_iter("reservations:*"):
        reservation_data = redis_client.get(key)
        if reservation_data:
            reservations.append(json.loads(reservation_data))
    return reservations

def fetch_vols():
    """Récupère tous les vols."""
    vols = []
    for key in redis_client.scan_iter("vols:*"):
        vol_data = redis_client.get(key)
        if vol_data:
            vols.append(json.loads(vol_data))
    return vols

def sort_and_merge(reservations, vols, join_key):
    """Trie et fusionne les réservations et les vols en fonction d'un attribut commun."""
    # Tri des réservations et des vols
    reservations.sort(key=lambda x: x['vol']['id'])  # Sort by vol id
    vols.sort(key=lambda x: x['id'])  # Sort by vol id

    merged_result = []
    i, j = 0, 0

    # Fusionner les deux listes triées
    while i < len(reservations) and j < len(vols):
        if reservations[i]['vol']['id'] == vols[j]['id']:
            merged_result.append(reservations[i])
            merged_result[-1]['vol'].update(vols[j])  # Ajouter les informations du vol
            i += 1
            j += 1
        elif reservations[i]['vol']['id'] < vols[j]['id']:
            i += 1
        else:
            j += 1

    return merged_result

def join_reservations_and_vols(redis_client, join_key='vol.id'):
    """Joint les réservations et les vols en utilisant une clé d'attribut commun."""
    reservations = fetch_reservations()
    vols = fetch_vols()

    if not vols:
        print("Aucun vol trouvé.")
        return []

    # Vérification si la clé d'attribut commun est valide
    if join_key != 'vol.id':
        print(f"Clé d'attribut non prise en charge: {join_key}")
        return []

    result = sort_and_merge(reservations, vols, join_key)
    return result

# Appel de la fonction de jointure
if __name__ == "__main__":
    resultat_jointure = join_reservations_and_vols(redis_client)
    print("Résultat de la jointure:")
    print(json.dumps(resultat_jointure, indent=4))
