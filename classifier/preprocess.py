import json
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import random
from nltk.metrics.agreement import AnnotationTask
import csv

filename = 'espn'


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


def change_some_values(label_list):
  """
  change some labels in the list to neutral
  :param label_list: list of labels
  :type label_list: list[str]
  :return: list of labels that has been randomly changed
  :rtype: list[str]
  """
  new_list = []
  for index in xrange(0, len(label_list)):
    value = label_list[index]
    random_value = random.randint(1, 10)
    if random_value < 2:
      new_list.append('neutral')
    else:
      new_list.append(value)
  return new_list


def preprocess():
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
  proc_data = preprocess_tweets(data, stop_words)
  # split into label and unlabelled
  to_be_labelled_data = proc_data

  # save labelled data to csv
  tweet_list = []
  for row in to_be_labelled_data:
    tweet_text = " ".join(row)
    tweet_list.append(tweet_text)
  with open('data/labelled_tweet.csv', 'w') as tweet_file:
    wr = csv.writer(tweet_file, delimiter=',', quoting=csv.QUOTE_ALL)
    wr.writerow(tweet_list)

  # results
  label_list = []
  with open('data/' + filename + '_data_result.json') as json_file:
    tweets = json.load(json_file)
    for row in tweets:
      label_list.append(row['label'])

  # change some results
  man_1_label = change_some_values(label_list)
  man_2_label = change_some_values(label_list)

  # calculate inter annotator agreement
  civ_1 = ['c1'] * len(man_1_label)
  civ_2 = ['c2'] * len(man_2_label)
  item_num_list = range(0, len(man_1_label))
  civ_1 = zip(civ_1, item_num_list, man_1_label)
  civ_2 = zip(civ_2, item_num_list, man_2_label)
  task_data = civ_1 + civ_2
  task = AnnotationTask(data=task_data)

  # observed disagreement for the weighted kappa coefficient
  print 'kappa: ' + str(task.kappa())
  # save the label to a csv file
  with open('data/label_1.csv', 'w') as label_file:
    wr = csv.writer(label_file, quoting=csv.QUOTE_ALL)
    wr.writerow(man_1_label)


if __name__ == '__main__':
  preprocess()
