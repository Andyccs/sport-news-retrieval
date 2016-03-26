from bs4 import BeautifulSoup
from common import save_to_csv
from nltk.corpus import stopwords
import json


def preprocess_tweets(data, stop_words):
  # convert to lower case
  processed_data = [sentence.lower() for sentence in data]
  # remove html
  processed_data = [BeautifulSoup(sentence, "html.parser").get_text()
                    for sentence in processed_data]
  # remove stopwords
  processed_data = [list.split() for list in processed_data]
  proc_data = []
  for list in processed_data:
    proc_list = [word for word in list if word not in stop_words]
    proc_data.append(proc_list)

  return proc_data


def preprocess(filename):
  # open file
  data = []
  with open('data/' + filename + '_data.json') as json_file:
    tweets = json.load(json_file)
    # load tweet data to a list
    for index, tweet in enumerate(tweets):
      text = tweet['text'].encode('ascii', 'ignore')
      data.append(text)

  # preprocess
  stop_words = stopwords.words('english')
  to_be_labelled_data = preprocess_tweets(data, stop_words)

  # save labelled data to csv
  tweet_list = []
  for row in to_be_labelled_data:
    tweet_text = " ".join(row)
    tweet_list.append(tweet_text)
  save_to_csv('data/labelled_tweet.csv', tweet_list)

  # save labels
  label_list = []
  with open('data/' + filename + '_data_result.json') as json_file:
    tweets = json.load(json_file)
    for row in tweets:
      label_list.append(row['label'])
  save_to_csv('data/label_api.csv', label_list)


if __name__ == '__main__':
  preprocess('espn')
