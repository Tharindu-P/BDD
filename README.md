# Guide d'installation et d'exécution des programmes

## Prérequis

Il faut avoir installer REDIS redis bloom ET MongoDB 


Dans chaque script python pour redis vérifier si la connexion au server redis est bonne pour VOTRE MACHINE car j'ai du changer le port de connexion (j'ai mis 6380)
pour mon cas sinon redis entrait en conflit avec mongodb et redis-bloom

Ensuite pour MongoDB et redisbloom l'installation a été faites via un docker donc verifiez aussi la connexion dans les scripts si elle est bonne pour votre machine


Assurez-vous que les fichiers de données sont dans le même répertoire que les scripts Python :

    PILOTES.txt
    CLIENTS.txt
    AVIONS.txt
    DEFCLASSES.txt
    VOLS.txt
    RESERVATIONS.txt

## Exécution des programmes

Chaque programme s'éxecute en faisant python3 nom du programme en étant DANS le répertoire "bdd"


1. Insérer les données dans Redis

Pour insérer les données dans Redis, exécutez le script main.py :

python3 main.py 

2. Insérer les données dans MongoDB

Ensuite, pour insérer les données dans MongoDB, exécutez le script mainmongo.py :

python3 mainmongo.py


# IMPORTANT

Pour les scripts GetPilotes,GetClient,GetVols : une fois éxecutez il faut choisir qu'une seule méthode de recherche (par id, nom etc)
Par exemple si vous souhaitez chercher par id pour GetPilotes il faudra écrire l'id lorsque c'est demandé et les autres info juste appuyer sur entrée

Exemple : 

tharindu@tharindu-VirtualBox:~/Bureau/bdd./bdd$ python3 getpilotes.py 
Veuillez entrer l'ID du pilote (ou autre pour ignorer): 
Veuillez entrer le nom du pilote (ou autre pour ignorer): dumas


//Réinitialisation des bases de données//

Si vous souhaitez réinitialiser Redis ou MongoDB avant d'exécuter les scripts (par exemple, si vous avez des données existantes et voulez repartir de zéro), 
voici comment procéder :
Réinitialiser Redis :

redis-cli flushall

Réinitialiser MongoDB :

mongo nomdelabd --eval "db.dropDatabase()"
