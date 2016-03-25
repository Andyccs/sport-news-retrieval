import classify, preprocess, linear_svc, gensim_classifier, ensemble_classifier, check_model_time

has_classified_data = True

if __name__ == '__main__':
  if not has_classified_data:
    classify.classify('espn')
    classify.classify('TheNBACentral')
  preprocess.preprocess()
  linear_svc.lin_svc()
  gensim_classifier.gensim_classifier()
  ensemble_classifier.ensemble_classify()
  check_model_time.find_and_save_timings()
