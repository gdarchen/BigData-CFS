import argparse
from server.server import Server


def evaluate_all(server):
    return serv


def print_results(valence, time, exceptions):
    print("Global valence:", valence)
    print("Computing time:", time, "seconds")
    print(len(exceptions), "errors occured")


def main(args):
    server = Server()
    print("Computing the valence...")
    if args.meantime:
        for
    if args.all:
        results = server.get_tweets_valence()
    else:
        tweet = server.tweets[args.tweet]
        print("Tweet text:", tweet.text)
        results = server.get_tweet_valence(tweet)
    print_results(*results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure the global opinion on Iron Man 3 on Twitter.")
    parser.add_argument("tweet", type=int, help="a Tweet ID")
    parser.add_argument("-a", "--all", action='store_true', help="compute on all Tweets")
    parser.add_argument("--meantime", type=int, nargs="?", const=3, help="compute the mean request time")
    parser.add_argument("--failrate", type=int, nargs="?", const=3, help="compute the mean failures rate")
    args = parser.parse_args()
    main(args)
