
import numpy as np
from data_source import get_labelled_tweets, get_labels, create_directory
from evaluation_metrics import evaluate, class_list
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.svm import LinearSVC


def save_model(model, file_name):
  """
  save model to the model folder
  """
  create_directory('model')
  joblib.dump(model, 'model/%s.pkl' % file_name)


def lin_svc():
  label_list = get_labels()
  tweet_list = get_labelled_tweets()
  # vectorise using tfid
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

  # train model and predict
  model = LinearSVC()
  ovr_classifier = OneVsRestClassifier(model).fit(train_vector, label_list[:index_value])
  result = ovr_classifier.predict(test_vector)

  # output result to csv
  temp_array = np.asarray(result)
  create_directory('data')
  result.tofile("data/log_reg_result.csv", sep=',')

  save_model(model, 'linear_svc')

  # evaluation
  label_score = ovr_classifier.decision_function(test_vector)
  binarise_result = label_binarize(result, classes=class_list)
  binarise_labels = label_binarize(label_list, classes=class_list)

  evaluate(binarise_result, binarise_labels[index_value:], label_score, 'tfid_linsvc_classifier')


if __name__ == '__main__':
  lin_svc()
