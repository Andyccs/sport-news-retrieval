from bs4 import BeautifulSoup
from common import save_to_csv
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import json
import nltk
import re
import string

lemmatizer = WordNetLemmatizer()


def wordnet_pos_code(tag):
  if tag == None:
    return ''
  elif tag.startswith('NN'):
    return wordnet.NOUN
  elif tag.startswith('VB'):
    return wordnet.VERB
  elif tag.startswith('JJ'):
    return wordnet.ADJ
  elif tag.startswith('RB'):
    return wordnet.ADV
  else:
    return ''


def transform_apostrophe(word, pos_tag):
  if word == "n't":
    word = "not"
  elif word == "'ll":
    word = "will"
  elif word == "'re":
    word = "are"
  elif word == "'ve":
    word = "have"
  elif word == "'s" and pos_tag == "VBZ":
    word = "is"
  return word


def preprocess_tweets(data, stop_words):
  # convert to lower case
  processed_data = [sentence.lower() for sentence in data]
  # remove html
  processed_data = [BeautifulSoup(sentence, "html.parser").get_text()
                    for sentence in processed_data]

  # split sentence to words
  processed_data = [sentence.split() for sentence in processed_data]

  tweet_list = []
  for sentence in processed_data:
    # Remove links
    sentence = [word for word in sentence if not re.match("^http\S+", word)]

    # Remove mention
    sentence = [word for word in sentence if not re.match("\S*@\S+", word)]

    # Remove hashtag
    sentence = [word for word in sentence if not re.match("\S*#\S+", word)]

    tweet_text = " ".join(sentence)
    tweet_list.append(tweet_text)

  # Lemmatization
  for i in range(len(tweet_list)):
    tweet = tweet_list[i]
    tokens = word_tokenize(tweet)

    preproccesed_string = []
    for (word, pos_tag) in nltk.pos_tag(tokens):
      word = transform_apostrophe(word, pos_tag)
      # Skip if it is stopwords
      if word in stop_words:
        continue
      elif pos_tag != None and pos_tag in [".", "TO", "IN", "DT", "UH", "WDT", "WP", "WP$", "WRB"]:
        continue

      if wordnet_pos_code(pos_tag) != "":
        word = lemmatizer.lemmatize(word, wordnet_pos_code(pos_tag))
      preproccesed_string.append(word)

    tweet_list[i] = " ".join(preproccesed_string)

  # Remove punctuation
  for i in range(len(tweet_list)):
    sentence = tweet_list[i]
    sentence = sentence.encode('utf-8').translate(string.maketrans("", ""), string.punctuation)
    tweet_list[i] = sentence

  return tweet_list


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
  tweet_list = preprocess_tweets(data, stop_words)

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
