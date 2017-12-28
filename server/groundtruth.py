class GroundTruth(object):
    """
        Class to represent a tuple in the ground truth table.
        It characterizes a tweet associated to its valence that was classified
        by hand.
    """

    def __init__(self, tweet = "", ground_truth_valence = 0):
        """
            Constructor to initiate the GroundTruth.
            tweet : the text of the tweet,
            ground_truth_valence : {-1 : negative | 0 : neutral | 1 : positive}.
        """
        self.__tweet = tweet
        self.__ground_truth_valence = ground_truth_valence

    @property
    def tweet(self):
        return self.__tweet

    @tweet.setter
    def tweet(self, tweet):
        self.__tweet = tweet

    @property
    def ground_truth_valence(self):
        return self.__ground_truth_valence

    @ground_truth_valence.setter
    def ground_truth_valence(self, ground_truth_valence):
        self.__ground_truth_valence = ground_truth_valence
    

    def __str__(self):
        return "tweet : %s \t ground_truth_valence : %s " % (self.tweet,
                                                    self.ground_truth_valence)
    def __repr__(self):
        return "GroundTruth(tweet=%s, ground_truth_valence=%s)" % (self.tweet,
                                                    self.ground_truth_valence)
