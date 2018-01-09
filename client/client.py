import argparse

# import sys
# sys.path.append('../')

from server.server import Server


def print_results(valence, time, exceptions):
    print("Valence:", valence)
    print("Computing time:", round(time, 6), "seconds")
    print("Error:", exceptions)


def main(args):
    server = Server()
    if args.quality:
        meantime, failrate = [], []
        tweets = server.tweets[:args.quality]
        for tw in tweets:
            time, fails = server.get_tweet_valence(tw.text)[1:]
            meantime.append(time)
            failrate.append(0 if fails is None else 1)
        meantime = sum(meantime) / len(meantime)
        failrate = sum(failrate) / len(failrate)
        f1 = server.compute_f1_score()
        print("Mean time per request:", round(meantime, 6), "seconds")
        print("Mean failure rate per request:", failrate)
        print("F1-score (macro average):", f1)
    else:
        if args.tweet:
            results = server.get_tweet_valence(args.tweet)
        else:
            results = server.compute_global_tweets_valence()
        print_results(*results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure the global opinion on Iron Man 3 on Twitter on a scale in [-1, 1].")
    parser.add_argument("tweet", metavar="SENTENCE", nargs="?", type=str, help="a sentence")
    parser.add_argument("-Q", "--quality", metavar="SAMPLES", type=int, nargs="?", const=100,
                        help="compute quality caracteristics: mean request time and mean failures rate")
    args = parser.parse_args()
    main(args)
