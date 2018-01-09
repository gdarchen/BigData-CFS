### INSA ROUEN 2017 — [CASI — Sujet 30A](http://prodageo.insa-rouen.fr/casi/sujetproj/sujetproj_30A_big_data_tweet.html)

# Big Data et tweet en temps réel — Solution CFS (*Cassandra File System*)

# Utilisation

## Installation et initialisation de l'environnement virtuel Python
A la racine du projet : 

```bash
# Création de l'environnement virtuel
$ python3 -m venv venv 
# Lancement de l'environnement virtuel
$ source venv/bin/activate
# Installation des dépendances dans l'environnement virtuel
(venv) $ pip install -r requirements
```

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

## Tests du serveur
Il est également possible de tester les fonctions du serveur. Pour cela, il faut suivre les instructions indiquées dans le fichier <kbd>server</kbd>><kbd>README.m</kbd>, pour créer les tables de test.

Ensuite, il est possible de lancer le script de test :
```bash
(venv) $ python3 -m server.test
```

## Technique étudiée

Analyse de données en flux continu (*streaming*) semi-structurées au moyen de technologies de la famille *Big Data*. 
L’architecture doit être capable de réaliser ce traitement rapidement (de l’ordre de quelques secondes) sur un gros volume de données (de l’ordre de quelques centaines de Mo)

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
