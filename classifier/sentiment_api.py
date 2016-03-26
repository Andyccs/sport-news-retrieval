import json
import urllib

LABEL_KEY = 'label'


def sentiment_api(filename):
  print 'Doing sentiment analysis for', filename

  with open('data/' + filename + '_data.json') as json_file:
    tweets = json.load(json_file)

  # do sentiment analysis
  for index, tweet in enumerate(tweets):
    # TODO(andyccs): current implementation is too slow, we just get the results of first
    # 10 sentiment analysis for testing purpose
    if index % 10 == 0 and index == 10:
      print 'processing: %.2f%%' % (float(index) / len(tweets) * 100.0)
      break

    text = tweet['text'].encode('ascii', 'ignore')
    data = urllib.urlencode({'text': text})
    result = urllib.urlopen('http://text-processing.com/api/sentiment/', data)
    json_data = json.loads(result.read())
    tweet[LABEL_KEY] = json_data[LABEL_KEY]

  with open('data/' + filename + '_data_sentiments.json', 'w') as tweets_sentiments_file:
    json.dump(tweets, tweets_sentiments_file)


if __name__ == '__main__':
  sentiment_api('espn')
