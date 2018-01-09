Ce document explique comment utiliser la partie *Docker* du projet **CASI—30A-BigData_CFS**.

# Création de fichiers textes contenant les tweets anglais des fichiers FlumeData contenus dans l'archive SentimentsFiles

Extraire SentimentsFiles.zip ainsi que SentimentsFiles/SentimentsFiles/tweets_raw_full.zip
Se placer dans le répertoire SentimentsFiles/SentimentsFiles/tweets_raw_full/tweets_raw et y copier les fichiers createFilesWithEnglishTweets.sh et flumetotxt.py. Puis lancer le script:

```bash
bash createFilesWithEnglishTweets.sh  
```

# Création conteneur docker
Installer docker si ce n'est pas déjà fait
```bash
sudo apt-get install docker.io
```

Executer les commandes suivantes :

```bash
docker pull store/datastax/dse-server:5.1.5
docker run -e DS_LICENSE=accept -e LISTEN_ADDRESS=172.17.0.2 --name my-dse -d -v /dse/cfs:/cfs store/datastax/dse-server:5.1.5 -kgs
#my dse est le nom du conteneur et /dse/cfs est le répertoire permettant de transférer des fichiers au répertoire /cfs du conteneur docker. LISTEN_ADDRESS est l'adresse IP du noeud.
```
## Changement du système de fichiers du conteneur pour obtenir CFS

Executer la commande suivante: 
```bash
#/path/to/file/ est le chemin menant au fichier core-site.xml
docker cp /path/to/file/core-site.xml my-dse:/opt/dse/resources/hadoop2-client/conf
```

## Création des tables Cassandra
Copier le fichier createKeyspace.cql dans /dse/cfs puis executer la commande suivante :

```bash
docker exec -it my-dse cqlsh -f /cfs/createKeyspace.cql
```

# Ecriture de tous les fichiers locaux dans CFS
Copier le fichier data/dictionary.tsv et data/ground_truth.tsv dans /dse/cfs puis exécuter les commandes suivantes :

```bash
docker exec -it my-dse dse hadoop fs -copyFromLocal /cfs/*.txt /
docker exec -it my-dse dse hadoop fs -mkdir /cfs
docker exec -it my-dse dse hadoop fs -copyFromLocal /cfs/dictionary.tsv /cfs
docker exec -it my-dse dse hadoop fs -copyFromLocal /cfs/ground_truth.tsv /cfs
```

# Ecriture des noms des fichiers texte CFS dans un fichier

```bash
docker exec -it my-dse dse hadoop fs -ls / > files.txt
grep -oP '/[a-zA-Z0-9.]*.txt' files.txt > CFSfiles.txt
```
# Création scala jar
Assurez-vous d'avoir installer scala version 2.11.6 et sbt version 1.0.4 :

```bash
sudo apt-get install scala
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
sudo apt-get update
sudo apt-get install sbt
```
Exécuter la commande suivante dans le répertoire ScalaApp/ :

```bash
sbt package
```
# Executer l'appli Scala avec Spark pour copier le contenu des fichiers CFS dans une base Cassandra.

Copier le jar produit (cfstocassandra_2.11-1.0.jar) dans /dse/cfs avec le fichier CFSfiles.txt créé précedemment puis exécuter la commande suivante :

```bash
docker exec -it my-dse dse spark-submit /cfs/cfstocassandra_2.11-1.0.jar /cfs/CFSfiles.txt /cfs/dictionary.tsv /cfs/ground_truth.tsv
```
