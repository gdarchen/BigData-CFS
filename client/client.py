import argparse

# import sys
# sys.path.append('../')

from server.server import Server


def print_results(valence, time, exceptions):
    print("Valence:", valence)
    print("Computing time:", round(time, 3), "seconds")
    print("Errors occured:", 0 if exceptions is None else len(exceptions))


def main(args):
    server = Server()
    if args.quality:
        meantime, failrate = [], []
        tweets = server.tweets[:args.quality]
        for i in range(args.quality):
            time, fails = server.get_tweet_valence(tweet)[1:]
            meantime.append(time)
            failrate.append(len(fails))
        meantime = sum(meantime) / len(meantime)
        failrate = sum(failrate) / len(failrate)
        print("Mean time per request:", meantime, "seconds")
        print("Mean failure rate per request:", failrate)
    if args.all:
        results = server.compute_global_tweets_valence()
    else:
        results = server.get_tweet_valence(args.tweet)
    print_results(*results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure the global opinion on Iron Man 3 on Twitter on a scale in [-1, 1].")
    parser.add_argument("tweet", metavar="SENTENCE", nargs="?", type=str, help="a sentence")
    parser.add_argument("-a", "--all", action="store_true", help="compute on all Tweets")
    parser.add_argument("-Q", "--quality", metavar="SAMPLES", type=int, nargs="?", const=100,
                        help="compute quality caracteristics: mean request time and mean failures rate")
    args = parser.parse_args()
    if not args.tweet and not args.all:
        raise ValueError("if not --all, a SENTENCE must be passed")

    main(args)
