class DictWord(object):
    """
        Class to represent a tuple in the dictionnary table.
        It characterizes a word according to its word text, 
        its valence and the strength of its valence (strong/weak).
    """

    def __init__(self, word = "", valence = 0, strength = ""):
        """
            Constructor to initiate the DictWord.
            word : the text of the word,
            valence : {-1 : negative | 0 : neutral | 1 : positive}.
        """
        self.__word = word
        self.__valence = valence
        self.__strength = strength

    @property
    def word(self):
        return self.__word

    @word.setter
    def word(self, word):
        self.__word = word

    @property
    def valence(self):
        return self.__valence

    @valence.setter
    def valence(self, valence):
        self.__valence = valence

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, strength):
        self.__strength = strength
    

    def __str__(self):
        return "word : %s \t valence : %s \t strength : %s " % (self.word,
                                                                self.valence,
                                                                self.strength)

    def __repr__(self):
        return "DictWord(word=%s, valence=%s, strength=%s)" % (self.word,
                                                               self.valence,
                                                               self.strength)
