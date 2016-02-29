import urllib
import json

LABEL_KEY = 'label'


def classify(filename):
  print 'Doing sentiment analysis for', filename

  with open(filename + '_data.json') as json_file:
    tweets = json.load(json_file)

  # do sentiment analysis
  for index, tweet in enumerate(tweets):
    if index % 10 == 0:
      print 'processing: %.2f%%' % (float(index) / len(tweets) * 100.0)

    text = tweet['text'].encode('ascii', 'ignore')
    data = urllib.urlencode({'text': text})
    result = urllib.urlopen('http://text-processing.com/api/sentiment/', data)
    json_data = json.loads(result.read())
    tweet[LABEL_KEY] = json_data[LABEL_KEY]

  with open(filename + '_data_sentiments.json', 'w') as tweets_sentiments_file:
    json.dump(tweets, tweets_sentiments_file)


if __name__ == '__main__':
  classify('espn')
  classify('TheNBACentral')
