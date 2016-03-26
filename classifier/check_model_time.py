from common import create_directory
from data_source import get_labelled_tweets
import timeit


def get_dataset_time(time, repetitions):
  """
  time to predict the full dataset
  """
  svm_time_dataset = time / repetitions
  return svm_time_dataset


def get_record_time(time, num_tweets):
  """
  time to predict 1 record only
  """
  svm_time_record = time / num_tweets
  return svm_time_record


def find_and_save_timings():
  tweet_list = get_labelled_tweets()
  num_tweets = len(tweet_list)

  setup = """
from data_source import get_labelled_tweets, get_labels;
from sklearn.externals import joblib;
tweet_list = get_labelled_tweets();
# do transformation into vector;
vectoriser = joblib.load('model/tfidf_vectoriser.pkl');
vectorised_tweet_list = vectoriser.transform(tweet_list);
svm_model = joblib.load('model/tfidf_linsvc.pkl');
svm_model.predict(vectorised_tweet_list);
"""

  test_statement = 'svm_model.predict(vectorised_tweet_list)'
  REPETITIONS = 100

  # check timing of svm
  # time in micro seconds
  svm_time = timeit.timeit(stmt=test_statement, setup=setup, number=REPETITIONS)
  svm_time_dataset = get_dataset_time(svm_time, REPETITIONS)
  svm_time_record = get_record_time(svm_time_dataset, num_tweets)

  setup_ensemble = """
import cPickle;
from data_source import get_labelled_tweets;
from sklearn.externals import joblib;

tweet_list = get_labelled_tweets();
vectoriser = joblib.load('model/tfidf_vectoriser.pkl');
vectorised_tweet_list = vectoriser.transform(tweet_list);
with open('model/tfidf_ada.pickle', 'rb') as f:
    ensemble_model = cPickle.load(f);
ensemble_model.predict(vectorised_tweet_list);
"""

  test_statement_ensemble = 'ensemble_model.predict(vectorised_tweet_list)'
  ensemble_time = timeit.timeit(stmt=test_statement_ensemble,
                                setup=setup_ensemble,
                                number=REPETITIONS)
  ens_time_dataset = get_dataset_time(ensemble_time, REPETITIONS)
  ens_time_record = get_record_time(ens_time_dataset, num_tweets)

  # save results in a txt file
  create_directory('metric_result')
  with open("metric_result/" + 'timings' + ".txt", "w") as text_file:
    text_file.write("Number of records in dataset: {0}\n".format(num_tweets))
    text_file.write("Svm dataset time: {0}\n".format(svm_time_dataset))
    text_file.write("Svm record time: {0}\n".format(svm_time_record))
    text_file.write("Ensemble dataset time: {0}\n".format(ens_time_dataset))
    text_file.write("Ensemble record time: {0}\n".format(ens_time_record))


if __name__ == '__main__':
  find_and_save_timings()
