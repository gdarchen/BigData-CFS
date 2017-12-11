# Installation des paquets du *virtual env*
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

# Ouverture de `cqlsh`
```bash
# Démarrage du service Cassandra (Mac)
$brew services start cassandra

# Démarrage de cqlsh
$ cqlsh
```

```sql
/* Création d'un KEYSPACE */
>>> CREATE KEYSPACE tmp WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

/* Utilisation du KEYSPACE créé */
>>> USE tmp;

/* Création de la table */
>>> CREATE TABLE tmp_table( id int PRIMARY KEY, name text, value text);

/* Insertion de tuples */
>>> INSERT INTO tmp_table(id, name, value) values (1, "nom 1", "valeur 1");
>>> INSERT INTO tmp_table(id, name, value) values (2, "nom 2", "valeur 2");
>>> INSERT INTO tmp_table(id, name, value) values (3, "nom 3", "valeur 3");
```

# Manipulation du `Cassandra-driver` de `Datastax` en Python
Documentation complète [**ici**](http://datastax.github.io/python-driver/getting_started.html).

```python
from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect('tmp')
rows = session.execute('SELECT * FROM tmp_table')
for row in rows:
    print(row)
```

