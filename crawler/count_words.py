import json

filenames = ['espn', 'TheNBACentral', 'SimpleNBAScores', 'ESPNNBA', 'NBATV']

total_words = 0
for filename in filenames:
  with open('data/' + filename + '_data.json') as json_file:
    tweets = json.load(json_file)
    # load tweet data to a list
    total_words += sum([len(tweet['text'].split()) for tweet in tweets])

print total_words