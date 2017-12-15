import json, sys, argparse
from collections import OrderedDict

if __name__ == "__main__":

    description = ('generate a JSON from the FlumeData File')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--flume-file', help='path of the FlumeData File')
    args = parser.parse_args()

    print("\n##################START\n")
    print("typing 'break' will exit the script and save the labeled texts\n")
    file_to_convert = args.flume_file
    new_json = OrderedDict()
    # FlumeData to Convert
    data = open(file_to_convert)

    for tweet in data:
        try:
            tweet_json = json.loads(tweet)
            # ignore the tweets that are not French or English
            if tweet_json['lang'] not in ['en','fr']:
                continue
            print(tweet_json['text'])
            # here you write the label for the text
            label = input("label (1, 0, -1)?  ")
            if label == "break":
                break
            new_json[tweet_json['text']] = label
        except KeyError:
            pass
    with open(args.flume_file+'.json', 'w') as outfile:
        json.dump(new_json, outfile, ensure_ascii=True)

    print("\n##################FINISH\n")