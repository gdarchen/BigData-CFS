import time
import numpy as np

from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory
from dictword import DictWord
from tweet import Tweet

class Odm(object):
    """
        Class manipulating the Cassandra database.
    """

    def __init__(self, keyspace = 'casi_test1'):
        """
            Initiates the Odm object, connecting it to a cluster with the 
            given keyspace.
            It also specializes the way to iterate on each tuple.
            
            keyspace : the Cassandra database keyspace
        """
        self.cluster = Cluster()
        self.session = self.cluster.connect(keyspace)
        self.session.row_factory = named_tuple_factory

    def get_tweets(self):
        """
            Reads every tweets stored in the database, build Tweet objects
            according to the read tweets and returns a list of each
            built Tweet.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        start = time.time()
        exception = None
        tweets = []

        try:
            rows = self.session.execute('SELECT * FROM tweets;')
            for row in rows:
                t = Tweet(text=row.tweet)
                tweets.append(t)
        except Exception as err:
            exception = str(err)

        end = time.time()
        elapsed_time = end - start
        return tweets, elapsed_time, exception

    def get_dict(self):
        """
            Reads every word stored in the dictionnary database, build 
            DictWord objects according to the read tuples and returns a 
            list of each built DictWord.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        start = time.time()
        exception = None
        words = []
        try:
            rows = self.session.execute('SELECT * FROM dict;')
            for row in rows:
                w = DictWord(word=row.word,
                            valence=row.valence,
                            strength=row.strength)
                words.append(w)
        except Exception as err:
            exception = str(err)
        
        end = time.time()
        elapsed_time = end - start
        return words, elapsed_time, exception