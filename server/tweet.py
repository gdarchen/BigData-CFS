class Tweet(object):
    """
        Class to represents a tuple in the tweets table.
        It characterizes a tweet according to its text.
    """

    def __init__(self, text = ""):
        """
            Constructor to initiate the Tweet.
            text : the text of the tweet.
        """
        self.__text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Tweet(text=%s)" % (self.text)
