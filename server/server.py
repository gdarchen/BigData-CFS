import time
import nltk
import numpy as np
from sklearn.metrics import f1_score

from server.odm import Odm
from server.dictword import DictWord
from server.tweet import Tweet
from server.tools import time_and_exception


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
        self.__tweets = self.odm.get_tweets()[0]
        self.__dict = self.odm.get_dict()[0]
        self.__ground_truth = self.odm.get_ground_truth()[0]

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
    
    @property
    def ground_truth(self):
        """
            List of all GroundTruth objects registered in the ground truth in 
            the DB.
        """
        return self.__ground_truth

    def print_tweets(self):
        """Prints every registered tweet."""
        for tweet in self.tweets:
            print(tweet)

    def print_dict(self):
        """Prints information about every registered word in the dictionnary."""
        for word in self.dict:
            print(word)

    @time_and_exception
    def tokenize_tweet(self, tweet):
        """Cuts the tweet and returns a list of lowercased tokens."""
        tokens = nltk.word_tokenize(tweet)
        tokens = [t.lower() for t in tokens]
        return tokens


    @time_and_exception
    def find_token_infos_in_dict(self, token):
        """
            Searches information about a token in the dictionnary.
            If the token is a word that is present in the dictionnary,
            it is returned.
            Else, 'None' is returned.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        for dict_word in self.dict:
            if (dict_word.word == token):
                return dict_word

        return None


    @time_and_exception
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
        tokens = self.tokenize_tweet(tweet)[0]
        global_valence = 0
        for token in tokens:
            dict_word = self.find_token_infos_in_dict(token)[0]
            if (dict_word is not None):
                global_valence += dict_word.valence \
                    if dict_word.strength == "strong" \
                    else dict_word.valence * 2

        global_valence = np.sign(global_valence)
        return global_valence

    @time_and_exception
    def get_tweets_valence(self):
        """
            Calculates the valence of each tweet of the database and returns
            a list of the calculated valences.

            It also returns the elapsed calculation time and the potential
            exception message.
        """
        general_valence = {}
        for tweet in self.tweets:
            general_valence[tweet.text] = self.get_tweet_valence(tweet)[0]

        return general_valence

    @time_and_exception
    def compute_global_tweets_valence():
        """
        Computes the global valence of the tweets database.

        :rtype: float in [-1, 1]
        :return: The global valence of the tweets database.
        """
        valences = self.get_tweets_valence()[0].values()
        return sum(valences) / len(valences)

    @time_and_exception
    def compute_f1_score(self):
        """
            Computes and returns the averaged macro F1-Score.
        """
        y_true = []
        y_pred =[]
        for g in self.ground_truth:
            # Store the true valence
            y_true.append(g.ground_truth_valence)
            
            # Compute the valence and store it too
            computed_val =  self.get_tweet_valence(g.tweet)[0]
            y_pred.append(computed_val)
        
        return f1_score(y_true, y_pred, average='macro')
