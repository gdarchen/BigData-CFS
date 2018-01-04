import json, sys, argparse
from collections import OrderedDict

if __name__ == "__main__":

    description = ('generate a JSON from the FlumeData File')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--flume-file', help='path of the FlumeData File')
    args = parser.parse_args()

    print("START")
    print("Labelling will stop when you've juged 200 tweets.")
    print("Labelling must answer the question \"Is the tweet positive, neutral or negative about Iron Man 3?\"")

    file_to_convert = args.flume_file
    new_json = OrderedDict()
    # FlumeData to Convert
    data = open(file_to_convert)

    no = 0
    for tweet in data:
        try:
            tweet_json = json.loads(tweet)
            # ignore the tweets that are not French or English
            if tweet_json['lang'] not in ['en','fr']:
                continue
            no += 1
            print("{}.".format(no), tweet_json['text'])
            # here you write the label for the text
            label = input("Label (1, 0 or -1):\t")
            if no == 200:
                break
            new_json[tweet_json['text']] = label
        except KeyError:
            pass
    with open(args.flume_file+'.json', 'w') as outfile:
        json.dump(new_json, outfile, ensure_ascii=True)

    print("\nFINISHED")
