from data_source import get_labelled_tweets, get_labels
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest

NGRAM = 2
NUMBER_OF_FEATURES = 1000


def to_weka_arff(ngram, number_of_features):
  count_vect = TfidfVectorizer(ngram_range=(1, ngram), norm='l2', sublinear_tf=True)

  label_list = get_labels()
  tweet_list = get_labelled_tweets()

  features = count_vect.fit_transform(tweet_list)

  features = SelectKBest(chi2, k=number_of_features).fit_transform(features, label_list)
  print features.shape

  arff_data = []

  arff_data.append("@RELATION sport")

  for i in range(features.shape[1]):
    arff_data.append("@ATTRIBUTE feature" + str(i) + " REAL")
  arff_data.append("@ATTRIBUTE sportclass {neutral,neg,pos}")

  arff_data.append("@DATA")

  array_features = features.toarray()
  for i in range(len(array_features)):
    feature = array_features[i]
    label = label_list[i]
    csv_feature = ",".join(str(x) for x in feature)
    csv_feature = csv_feature + "," + label
    arff_data.append(csv_feature)

  with open('data/sport.arff', 'w') as file:
    for item in arff_data:
      file.write("%s\n" % item)


if __name__ == '__main__':
  to_weka_arff(NGRAM, NUMBER_OF_FEATURES)
