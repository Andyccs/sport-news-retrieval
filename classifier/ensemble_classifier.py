import numpy as np
from data_source import get_labelled_tweets, get_labels, create_directory
from evaluation_metrics import class_list, generate_eval_metrics
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import label_binarize


def save_model(model, file_name):
  """
  save model to the model folder
  """
  create_directory('model')
  joblib.dump(model, 'model/%s.pkl' % file_name)


def ensemble_classify():
  label_list = get_labels()
  tweet_list = get_labelled_tweets()
  # vectorise using tf-idf
  vectoriser = TfidfVectorizer(min_df=3,
                               max_features=None,
                               strip_accents='unicode',
                               analyzer='word',
                               token_pattern=r'\w{1,}',
                               ngram_range=(1, 2),
                               use_idf=1,
                               smooth_idf=1,
                               sublinear_tf=1,)

  ## do transformation into vector
  vectoriser.fit(tweet_list)
  vectorised_tweet_list = vectoriser.transform(tweet_list)
  index_value = int(len(tweet_list) * 0.8)  # 0.8 percent for training set
  train_vector = vectorised_tweet_list[:index_value]
  test_vector = vectorised_tweet_list[index_value:]

  n_estimators = 10  # number of weak learners
  model = AdaBoostClassifier(n_estimators=n_estimators)
  ada_classifier = model.fit(train_vector, label_list[:index_value])
  result = ada_classifier.predict(test_vector)

  # output result to csv
  create_directory('data')
  result.tofile("data/ensemble_ada_result.csv", sep=',')

  save_model(ada_classifier, 'ensemble_ada_classifier')

  # evaluation
  binarise_result = label_binarize(result, classes=class_list)
  binarise_labels = label_binarize(label_list, classes=class_list)
  generate_eval_metrics(binarise_result, 'ensemble_ada', binarise_labels[index_value:])
