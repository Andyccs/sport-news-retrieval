import classify, preprocess, linear_svc, gensim_classifier

has_classified_data = True

if __name__ == '__main__':
  if not has_classified_data:
    classify.classify('espn')
    classify.classify('TheNBACentral')
  preprocess.preprocess()
  linear_svc.lin_svc()
  gensim_classifier.gensim_classifier()
