import argparse

import sys
sys.path.append('../')

from server.server import Server


def print_results(valence, time, exceptions):
    print("Global valence:", valence)
    print("Computing time:", time, "seconds")
    print(len(exceptions), "errors occured")


def main(args):
    server = Server()
    print("Computing the valence...")
    if args.meantime_failrate:
        meantime, failrate = [], []
        tweets = server.tweets[:args.meantime_failrate]
        for i in range(args.meantime_failrate):
            time, fails = server.get_tweet_valence(tweet)[1:]
            meantime.append(time)
            failrate.append(len(fails))
        meantime = sum(meantime) / len(meantime)
        failrate = sum(failrate) / len(failrate)
        print("Mean time per request:", meantime, "seconds")
        print("Mean failure rate per request:", failrate)
    if args.all:
        results = server.get_tweets_valence()
    else:
        tweet = server.tweets[args.tweet]
        print("Tweet text:", tweet.text)
        results = server.get_tweet_valence(tweet)
    print_results(*results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure the global opinion on Iron Man 3 on Twitter on a scale in [-1, 1].")
    parser.add_argument("tweet", nargs="*", type=int, help="a tweet ID")
    parser.add_argument("-a", "--all", action='store_true', help="compute on all Tweets")
    parser.add_argument("-Q", "--quality", type=int, nargs="?", const=100,
                        help="compute quality caracteristics: mean request time and mean failures rate")
    args = parser.parse_args()
    main(args)
