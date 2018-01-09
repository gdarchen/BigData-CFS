CREATE KEYSPACE casi_test1 WITH replication = {'class': 'NetworkTopologyStrategy', 'SearchGraphAnalytics': '1'}

/* Utilisation du KEYSPACE créé */
USE casi_test1;

/* Création des tables */
CREATE TABLE tweets(id timeuuid PRIMARY KEY, tweet text);
CREATE TABLE dict(word text PRIMARY KEY, valence int, strength text);
CREATE TABLE ground_truth(tweet text PRIMARY KEY, ground_truth_valence int);
