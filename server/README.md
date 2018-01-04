Ce document explique comment utiliser la partie *Serveur* du projet **CASI—30A-BigData_CFS**.

**Toutes les classes sont documentées, n'hésitez donc pas à fouiller dans le code si une information est manquante.**


# Installation des paquets du *virtual env*
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

# pour quitter le venv à la fin, faire : $ deactivate
```

# Initialisation de la base de données Cassandra

## Démarrage du service et lancement de `cqlsh`
```bash
# Démarrage du service Cassandra (Mac)
$ brew services start cassandra

# Démarrage de cqlsh
$ cqlsh
```

## Création des tables Cassandra
```sql
/* Création d'un KEYSPACE */
>>> CREATE KEYSPACE casi_test1 WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

/* Utilisation du KEYSPACE créé */
>>> USE casi_test1;

/* Création des tables */
>>> CREATE TABLE tweets(tweet text PRIMARY KEY);
>>> CREATE TABLE dict(word text PRIMARY KEY, valence int, strength text);
>>> CREATE TABLE ground_truth(tweet text PRIMARY KEY, ground_truth_valence int);

/* Insertion de tuples */
>>> INSERT INTO dict(word, valence, strength) values ('anti', -1, 'strong');
>>> INSERT INTO dict(word, valence, strength) values ('shit', -1, 'strong');
>>> INSERT INTO dict(word, valence, strength) values ('crazy', 1, 'strong');
>>> INSERT INTO dict(word, valence, strength) values ('good', 1, 'strong');

>>> INSERT INTO tweets(tweet) VALUES('Iron Man 3 is such a shit');
>>> INSERT INTO tweets(tweet) values('I found Iron Man 3 was a crazy film') ;
>>> INSERT INTO tweets(tweet) values('I have never seen such a good film before') ;
>>> INSERT INTO tweets(tweet) values('I am not convinced by this shit film...') ;

>>> INSERT INTO ground_truth(tweet, ground_truth_valence) VALUES ('I am not convinced by this shit film...', -1);
>>> INSERT INTO ground_truth(tweet, ground_truth_valence) VALUES ('Iron Man 3 is such a shit', -1);
>>> INSERT INTO ground_truth(tweet, ground_truth_valence) VALUES ('I found Iron Man 3 was a crazy film', 1);
>>> INSERT INTO ground_truth(tweet, ground_truth_valence) VALUES ('I have never seen such a good film before', 1);

/* Tables souhaitées */
>>> SELECT * from casi_test1.dict;

 word  | strength | valence
-------+----------+---------
  good |   strong |       1
  shit |   strong |      -1
   not |   strong |      -1
 crazy |   strong |       1
  anti |   strong |      -1


>>> SELECT * from casi_test1.tweets;

 tweet
-------------------------------------------
   I am not convinced by this shit film...
                 Iron Man 3 is such a shit
       I found Iron Man 3 was a crazy film
 I have never seen such a good film before

>>> SELECT * FROM casi_test1.ground_truth;

 tweet                                     | ground_truth_valence
-------------------------------------------+----------------------
   I am not convinced by this shit film... |                   -1
                 Iron Man 3 is such a shit |                   -1
       I found Iron Man 3 was a crazy film |                    1
 I have never seen such a good film before |                    1
```

# Utilisation des classes
Le fichier `test.py` présente une utilisation possible des classes du serveur. 

Un résultat donné par ce script est le suivant : 
```bash
$ python server/test.py

---------------- Tweets ----------------
I am not convinced by this shit film...
Iron Man 3 is such a shit
I found Iron Man 3 was a crazy film
I have never seen such a good film before

----------------- Dict -----------------
word : good 	 valence : 1 	 strength : strong
word : shit 	 valence : -1 	 strength : strong
word : not 	 valence : -1 	 strength : strong
word : crazy 	 valence : 1 	 strength : strong
word : anti 	 valence : -1 	 strength : strong

------------- Tokenization -------------
['i', 'am', 'not', 'convinced', 'by', 'this', 'shit', 'film', '...']
['iron', 'man', '3', 'is', 'such', 'a', 'shit']
['i', 'found', 'iron', 'man', '3', 'was', 'a', 'crazy', 'film']
['i', 'have', 'never', 'seen', 'such', 'a', 'good', 'film', 'before']

------------ Global valence ------------
I am not convinced by this shit film... : valence = -1
Iron Man 3 is such a shit : valence = -1
I found Iron Man 3 was a crazy film : valence = 1
I have never seen such a good film before : valence = 1

--------------- F1-Score ---------------
1.0
```

Explications du programme : 
1. Affichage de tous les tweets stockés.
2. Affichage des informations sur tous les mots enregistrés dans le dictionnaire.
3. Affichage des *tokens* issus du découpage des mots de chacun des tweets.
4. Résultat de la valence globale de chaque tweet.
5. Calcul du F1-Score moyen pour chacune des classes.

# Bibliographie 

- Manipulation du `Cassandra-driver` de `Datastax` en Python : 
[**documentation complète**](http://datastax.github.io/python-driver/getting_started.html).


