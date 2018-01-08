class Tweet(object):
    """
        Class to represent a tuple in the tweets table.
        It characterizes a tweet according to its text.
    """

    def __init__(self, id, text = ""):
        """
            Constructor to initiate the Tweet.
            id : the TIMEUUID of the tweet.
            text : the text of the tweet.
        """
        self.__id = id
        self.__text = text

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Tweet(id=%s, text=%s)" % (self.id, self.text)
