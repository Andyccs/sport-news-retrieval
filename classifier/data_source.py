import os
import csv

def get_labels():
  with open('data/label_1.csv', 'r') as label_file:
    reader = csv.reader(label_file)
    label_list = list(reader)[0]
  return label_list


def get_labelled_tweets():
  with open('data/labelled_tweet.csv', 'r') as label_file:
    reader = csv.reader(label_file)
    tweet_list = list(reader)[0]
  return tweet_list


def train_test_split(percentage, data_set):
  # split data into training and test set
  index_value = int(len(data_set) * percentage)
  train_vector = data_set[:index_value]
  test_vector = data_set[index_value:]

  return index_value, train_vector, test_vector


def create_directory(data):
  try:
    os.makedirs(data)
  except OSError:
    if not os.path.isdir(data):
      raise
