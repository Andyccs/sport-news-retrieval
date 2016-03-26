from common import create_directory
from data_source import get_labelled_tweets, get_labels, train_test_split
from evaluation_metrics import evaluate, class_list
from gensim.models.word2vec import Word2Vec
from sklearn.externals import joblib
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.svm import LinearSVC
import csv
import logging
import numpy as np


def makeFeatureVec(list_word, model, num_features):
  """
  Averages the word vectors for a sentence
  """
  feature_vector = np.zeros((num_features,), dtype="float32")
  index2word_set = set(model.index2word)
  # check if in model's vocab, add vector to total
  nwords = 0
  for word in list_word:
    if word in index2word_set:
      nwords = nwords + 1.
      feature_vector = np.add(feature_vector, model[word])

  # Divide the result by the number of words to get the average
  feature_vector = np.divide(feature_vector, nwords)
  return feature_vector


def getAvgFeatureVecs(sentence_list, model, num_features):
  """
  Calculate average feature vector for each sentence
  """
  av_vector_list = np.zeros((len(sentence_list), num_features), dtype="float32")
  counter = 0
  for review in sentence_list:
    if counter % 50. == 0:
      print "Sentence %d of %d" % (counter, len(sentence_list))
    av_vector_list[counter] = makeFeatureVec(review, model, num_features)
    counter = counter + 1
  return av_vector_list


def gensim_classifier():
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
  label_list = get_labels()
  tweet_list = get_labelled_tweets()

  # split all sentences to list of words
  sentences = []
  for tweet in tweet_list:
    temp_doc = tweet.split()
    sentences.append(temp_doc)

  # parameters for model
  num_features = 100
  min_word_count = 1
  num_workers = 4
  context = 2
  downsampling = 1e-3

  # Initialize and train the model
  w2v_model = Word2Vec(sentences, workers=num_workers, \
              size=num_features, min_count = min_word_count, \
              window = context, sample = downsampling, seed=1)

  index_value, train_set, test_set = train_test_split(0.80, sentences)
  train_vector = getAvgFeatureVecs(train_set, w2v_model, num_features)
  test_vector = getAvgFeatureVecs(test_set, w2v_model, num_features)

  # train model and predict
  model = LinearSVC()
  classifier_fitted = OneVsRestClassifier(model).fit(train_vector, label_list[:index_value])
  result = classifier_fitted.predict(test_vector)

  # output result to csv
  create_directory('data')
  result.tofile("data/word2vec_linsvc_result.csv", sep=',')

  # store the model to mmap-able files
  create_directory('model')
  w2v_model.save('model/word2vec_model.doc2vec')
  joblib.dump(model, 'model/%s.pkl' % 'w2v_linsvc')

  # evaluation
  label_score = classifier_fitted.decision_function(test_vector)
  binarise_result = label_binarize(result, classes=class_list)
  binarise_labels = label_binarize(label_list, classes=class_list)

  evaluate(binarise_result, binarise_labels[index_value:], label_score, 'gensim_classifier')


if __name__ == '__main__':
  gensim_classifier()
