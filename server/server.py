import time
import nltk
import numpy as np

from odm import Odm
from dictword import DictWord
from tweet import Tweet


class Server(object):
    """
        Class making some operations on the tweet database.
        It can tokenize a tweet, interact with an ODM and 
        calculate the global valence of a tweet according
        to a dictionnary.
    """

    def __init__(self):
        """
            Constructor for a Server object.
            It initializes the ODM to interact with the DB, get the 
            tweets list and the dictionnary.
        """
        self.__odm = Odm()
        self.__tweets,_,_ = self.odm.get_tweets()
        self.__dict,_,_ = self.odm.get_dict()
    
    @property
    def odm(self):
        """ODM object to manage the interaction with the DB."""
        return self.__odm

    @property
    def tweets(self):
        """List of all tweets registered in the DB."""
        return self.__tweets

    @property
    def dict(self):
        """List of all DictWord registered in the dictionnary in the DB."""
        return self.__dict
    
    def print_tweets(self):
        """Prints every registered tweet."""
        for tweet in self.tweets:
            print(tweet)

    def print_dict(self):
        """Prints information about every registered word in the dictionnary."""
        for word in self.dict:
            print(word)
    
    def tokenize_tweet(self, tweet):
        """Cuts the tweet and returns a list of lowercased tokens."""
        start = time.time()
        exception = None
        tokens = []
        try:
            tokens = nltk.word_tokenize(tweet)
            tokens = [t.lower() for t in tokens]
        except Exception as err: 
            exception = str(err)
            
        end = time.time()
        elapsed_time = end - start
        return tokens, elapsed_time, exception
            
    def find_token_infos_in_dict(self, token):
        """
            Searches information about a token in the dictionnary.
            If the token is a word that is present in the dictionnary, 
            it is returned.
            Else, '-1' is returned.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        start = time.time()
        exception = None
        res = -1
        try:
            for dict_word in self.dict:
                    if (dict_word.word == token):
                        res = dict_word
                        break
        except Exception as err:
            exception = str(err)
        
        end = time.time()
        elapsed_time = end - start

        return res, elapsed_time, exception

    
    def get_tweet_valence(self, tweet):
        """
            Calculates and returns the global valence of a given tweet.
            For each token of the tweet, it searches information about it 
            in the dictionnary. If such information are found, we look at
            the valence of the token to update the tweet global valence.

            On top of that, if the strength of the word is 'strong', we 
            ponderate its valence by 2.

            After all, we return the global valence of the tweet as the sign 
            of the previously calculated valence.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        start = time.time()
        exception = None

        try:
            tokens,_,_ = self.tokenize_tweet(tweet)
            global_valence = 0
            for token in tokens:
                dict_word,_,_ = self.find_token_infos_in_dict(token)
                if (dict_word != -1):
                    global_valence += dict_word.valence\
                        if dict_word.strength=="weak"\
                        else dict_word.valence*2
            
            global_valence = np.sign(global_valence)
        except Exception as err:
            exception = str(err)

        end = time.time()
        elapsed_time = end - start
        return global_valence, elapsed_time, exception

    def get_tweets_valence(self):
        """
            Calculates the valence of each tweet of the database and returns
            a list of the calculated valences.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        start = time.time()
        exception = None
        general_valence = {}
        try:
            for tweet in self.tweets:
                general_valence[tweet.text],_,_ = self.get_tweet_valence(tweet)
        except Exception as err:
            exception = str(err)
        
        end = time.time()
        elapsed_time = end - start
        return general_valence, elapsed_time, exception