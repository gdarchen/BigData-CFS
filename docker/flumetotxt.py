import json, sys, argparse

if __name__ == "__main__":

    description = ('generate a file from the FlumeData File with only english tweets')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--flume-file', help='path of the FlumeData File')
    args = parser.parse_args()
    file_to_convert = args.flume_file
    # FlumeData to Convert
    with open(file_to_convert) as data:
        with open(args.flume_file+'.txt', "w") as f1:
            for tweet in data:
	        try:
                    tweet_json = json.loads(tweet)
                    # ignore the tweets that are not English
                    if tweet_json['lang'] not in ['en']:
                        continue
	            f1.write(tweet_json['text'].encode("utf-8")+"\t")
		except KeyError:
		    pass


