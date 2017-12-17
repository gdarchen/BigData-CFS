import time
import numpy as np

from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory
from server.dictword import DictWord
from server.tweet import Tweet
from server.tools import time_and_exception


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

    @time_and_exception
    def get_tweets(self):
        """
            Reads every tweets stored in the database, build Tweet objects
            according to the read tweets and returns a list of each
            built Tweet.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        tweets = []
        rows = self.session.execute('SELECT * FROM tweets;')
        for row in rows:
            t = Tweet(text=row.tweet)
            tweets.append(t)
        return tweets

    @time_and_exception
    def get_dict(self):
        """
            Reads every word stored in the dictionnary database, build
            DictWord objects according to the read tuples and returns a
            list of each built DictWord.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        words = []
        rows = self.session.execute('SELECT * FROM dict;')
        for row in rows:
            w = DictWord(word=row.word,
                        valence=row.valence,
                        strength=row.strength)
            words.append(w)
        return words
