from server.server import Server 

def main():
    print("\n")
    s = Server()
    print("---------------- Tweets ----------------")
    s.print_tweets()

    print("\n")

    print("----------------- Dict -----------------")
    s.print_dict()

    print("\n")
    print("------------- Tokenization -------------")
    tokens = {}
    for tweet in s.tweets:
        t = s.tokenize_tweet(tweet.text)[0]
        tokens[tweet.text] = t
        print(t)
    print("\n")

    print("------------ Global valence ------------")
    for tweet in s.tweets:
        print("%s : valence = %d"%(tweet.text, s.get_tweet_valence(tweet.text)[0]))
    print("\n")



if __name__ == '__main__':
    main()
