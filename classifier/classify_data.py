from sklearn.externals import joblib
import json

filenames = ['espn', 'TheNBACentral', 'SimpleNBAScores', 'ESPNNBA', 'NBATV']
ALL_DATA_FILE_PATH = 'data/all_data.json'
LABEL_KEY = 'label'


def classify_data():
  model = joblib.load('model/linear_svc.pkl')
  vectoriser = joblib.load('model/tf_idf_vectoriser.pkl')

  all_tweets_with_metadata = []
  all_tweets = []
  for filename in filenames:
    with open('data/' + filename + '_data.json') as json_file:
      tweets_with_metadata = json.load(json_file)
      tweets = [tweet_with_metadata['text'] for tweet_with_metadata in tweets_with_metadata]

      all_tweets_with_metadata.extend(tweets_with_metadata)
      all_tweets.extend(tweets)

  vectorised_data = vectoriser.transform(all_tweets)
  labels = model.predict(vectorised_data)

  for tweet, label in zip(all_tweets_with_metadata, labels):
    tweet[LABEL_KEY] = label

  with open(ALL_DATA_FILE_PATH, 'w') as all_data_file:
    json.dump(all_tweets_with_metadata, all_data_file)


if __name__ == '__main__':
  classify_data()
