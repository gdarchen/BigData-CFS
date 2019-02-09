# BigData-CFS

At INSA Rouen, we worked with Cassandra File System so as to analyze a big amount of tweets and evualuate a global valence.

We are then able to say if the majority of the people who have tweeted are for or against a given subject.

## Big Data et tweet en temps réel — Solution CFS (*Cassandra File System*)

Analyse de données en flux continu (*streaming*) semi-structurées au moyen de technologies de la famille *Big Data*. 
L’architecture doit être capable de réaliser ce traitement rapidement (de l’ordre de quelques secondes) sur un gros volume de données (de l’ordre de quelques centaines de Mo)

### Utilisation

#### Installation et initialisation de l'environnement virtuel Python
A la racine du projet : 

```bash
# Création de l'environnement virtuel
$ python3 -m venv venv 
# Lancement de l'environnement virtuel
$ source venv/bin/activate
# Installation des dépendances dans l'environnement virtuel
(venv) $ pip install -r requirements
```

## Serveur

Cette partie explique comment utiliser la partie *Serveur* du projet **BigData_CFS**.

**Toutes les classes sont documentées, n'hésitez donc pas à fouiller dans le code si une information est manquante.**


### Installation des paquets du *virtual env*
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# pour quitter le venv à la fin, faire : $ deactivate
```

### Initialisation de la base de données Cassandra

#### Démarrage du service et lancement de `cqlsh`
```bash
# Démarrage du service Cassandra (Mac)
brew services start cassandra

# Démarrage de cqlsh
cqlsh
```

#### Création des tables Cassandra
```sql
/* Création d'un KEYSPACE */
CREATE KEYSPACE casi_test1 WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};

/* Utilisation du KEYSPACE créé */
USE casi_test1;

/* Création des tables */
CREATE TABLE tweets(id TIMEUUID PRIMARY KEY, tweet text);
CREATE TABLE dict(word text PRIMARY KEY, valence int, strength text);
CREATE TABLE ground_truth(tweet text PRIMARY KEY, ground_truth_valence int);

/* Insertion de tuples */
INSERT INTO dict(word, valence, strength) values ('anti', -1, 'strong');
INSERT INTO dict(word, valence, strength) values ('shit', -1, 'strong');
INSERT INTO dict(word, valence, strength) values ('crazy', 1, 'strong');
INSERT INTO dict(word, valence, strength) values ('good', 1, 'strong');

INSERT INTO tweets(id, tweet) VALUES(now(), 'Iron Man 3 is such a shit');
INSERT INTO tweets(id, tweet) VALUES(now(), 'I found Iron Man 3 was a crazy film');
INSERT INTO tweets(id, tweet) VALUES(now(), 'I have never seen such a good film before');
INSERT INTO tweets(id, tweet) VALUES(now(), 'I am not convinced by this shit film...');

INSERT INTO ground_truth(tweet, ground_truth_valence) VALUES ('I am not convinced by this shit film...', -1);
INSERT INTO ground_truth(tweet, ground_truth_valence) VALUES ('Iron Man 3 is such a shit', -1);
INSERT INTO ground_truth(tweet, ground_truth_valence) VALUES ('I found Iron Man 3 was a crazy film', 1);
INSERT INTO ground_truth(tweet, ground_truth_valence) VALUES ('I have never seen such a good film before', 1);

/* Tables souhaitées */
SELECT * from casi_test1.dict;

 word  | strength | valence
-------+----------+---------
  good |   strong |       1
  shit |   strong |      -1
   not |   strong |      -1
 crazy |   strong |       1
  anti |   strong |      -1


SELECT * from casi_test1.tweets;

 id                                   | tweet
--------------------------------------+-------------------------------------------
 aaa16ca0-f4a0-11e7-86e3-2d6f566e575a |       I found Iron Man 3 was a crazy film
 afe95a60-f4a0-11e7-86e3-2d6f566e575a | I have never seen such a good film before
 b2f49e90-f4a0-11e7-86e3-2d6f566e575a |   I am not convinced by this shit film...
 8ebf83f0-f4a0-11e7-86e3-2d6f566e575a |                 Iron Man 3 is such a shit

SELECT * FROM casi_test1.ground_truth;

 tweet                                     | ground_truth_valence
-------------------------------------------+----------------------
   I am not convinced by this shit film... |                   -1
                 Iron Man 3 is such a shit |                   -1
       I found Iron Man 3 was a crazy film |                    1
 I have never seen such a good film before |                    1
```

### Utilisation des classes
Le fichier `test.py` présente une utilisation possible des classes du serveur.

Un résultat donné par ce script est le suivant :
```bash
python -m server.test

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

## Bibliographie

- Manipulation du `Cassandra-driver` de `Datastax` en Python :
[**documentation complète**](http://datastax.github.io/python-driver/getting_started.html).


## Client
Pour utiliser le client, il faut se placer à la racine du projet. Les options, affichées par l'aide (option `-h`) sont les suivantes :
```bash
(venv) $ python3 -m client.client -h                                                                                                                                   
usage: client.py [-h] [-Q [SAMPLES]] [SENTENCE]

Measure the global opinion on Iron Man 3 on Twitter on a scale in [-1, 1].

positional arguments:
  SENTENCE              a sentence

optional arguments:
  -h, --help            show this help message and exit
  -Q [SAMPLES], --quality [SAMPLES]
                        compute quality caracteristics: mean request time and
                        mean failures rate
```

On peut donc :

* Lancer le client sans argument, auquel cas cela traite l'intégralité des données (`(venv) $ python3 -m client.client`)
* Lancer le client avec l'argument `-Q` pour calculer les métriques des facteurs qualité (`(venv) $ python3 -m client.client -Q`)
* Lancer le client avec une phrase à évaluer (`(venv) $ python3 -m client.client "Iron Man was such a shit"`)


## Contexte
### Cas d’utilisation 1

Etude des comportements des jeunes diplomés sur la base de leur activité publique sur les réseaux sociaux (par exemple un flux Twitter) : 
l’objectif est d’évaluer une tendance (positive, négative) sur un sujet par une technique simple consistant à compter le nombre de mots 
dits négatifs et positifs contenus dans un flux de *tweets* (au moyen d’un dictionnaire qui valorise positivement / négativement chacun 
des termes qu’il contient).

### Contexte technique

Un flux *tweets* significatif sera fourni à titre d’exemple (en l’absence de *tweets* concernant ASI, nous utiliserons un [flux dédié au 
lancement de IronMan3](http://s3.amazonaws.com/hw-sandbox/tutorial13/SentimentFiles.zip). 

Ce zip contient 3 fichiers :

 - `tweets` - which contains tweets
 - `time_zone_map` - which contains the country name to time zone mapping
 - `dictionary` - the list of positive and negative words

**Note :** [emplacement nominal du fichier `SentimentFiles.zip`](http://s3.amazonaws.com/hw-sandbox/tutorial13/SentimentFiles.zip) / [emplacement de secours du fichier `SentimentFiles.zip`](http://casisbelli-03.insa-rouen.fr/casi/ressources/sujetproj/13A/SentimentFiles.zip)

## Questions d’amorce

- On prendra soin de définir le terme grappe (*cluster*) ainsi que les différents types de grappes : grappe haute-disponibilité (HA cluster et ses différentes configurations), 
  grappe à équilibrage de charge (*load-balancing cluster*), grappe de calcul (*compute cluster* ou *HPC cluster*) et grille de calcul (*grid computing*).
- Définir l’architecture de l’écosystème *Hadoop* (`Hive`, `Pig`, `Flume`, `Oozie`, `Impala`, …) : comment s’articule cet ensemble d’outils pour composer une architecture *Big Data*. On pourrait aussi analyser l’offre de `Talend`
