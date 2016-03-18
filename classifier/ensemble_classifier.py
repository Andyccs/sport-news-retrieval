import cPickle
from data_source import get_labelled_tweets, get_labels, create_directory
from evaluation_metrics import class_list, generate_eval_metrics
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import label_binarize


def save_model(model, file_name):
  """
  save model to the model folder
  """
  create_directory('model')
  with open('model/%s.pickle' % file_name, 'wb') as f:
    cPickle.dump(model, f)


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
  train_vector, test_vector, train_labels, test_labels = train_test_split(vectorised_tweet_list,
                                                                          label_list,
                                                                          test_size=0.8,
                                                                          random_state=42)

  n_estimators = 10  # number of weak learners
  model = AdaBoostClassifier(n_estimators=n_estimators)
  ada_classifier = model.fit(train_vector, train_labels)
  result = ada_classifier.predict(test_vector)

  # output result to csv
  create_directory('data')
  result.tofile("data/ensemble_ada_result.csv", sep=',')
  save_model(ada_classifier, 'ensemble_ada_classifier')

  # evaluation
  binarise_result = label_binarize(result, classes=class_list)
  binarise_labels = label_binarize(test_labels, classes=class_list)
  generate_eval_metrics(binarise_result, 'ensemble_ada', binarise_labels)


if __name__ == '__main__':
  ensemble_classify()
