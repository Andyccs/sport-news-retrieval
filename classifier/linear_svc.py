from data_source import get_labelled_tweets, get_labels, create_directory
from evaluation_metrics import evaluate, class_list
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split


def save_model(model, file_name):
  """
  save model to the model folder
  """
  create_directory('model')
  joblib.dump(model, 'model/%s.pkl' % file_name)


def lin_svc():
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

  # train model and predict
  model = LinearSVC()
  ovr_classifier = OneVsRestClassifier(model).fit(train_vector, train_labels)
  result = ovr_classifier.predict(test_vector)

  # output result to csv
  create_directory('data')
  result.tofile("data/log_reg_result.csv", sep=',')

  save_model(model, 'linear_svc')

  # evaluation
  label_score = ovr_classifier.decision_function(test_vector)
  binarise_result = label_binarize(result, classes=class_list)
  binarise_labels = label_binarize(test_labels, classes=class_list)

  evaluate(binarise_result, binarise_labels, label_score, 'tfid_linsvc_classifier')


if __name__ == '__main__':
  lin_svc()
