from common import save_to_csv
from nltk.metrics.agreement import AnnotationTask
import json
import random


def change_some_values(label_list):
  """
  change some labels in the list to neutral
  :param label_list: list of labels
  :type label_list: list[str]
  :return: list of labels that has been randomly changed
  :rtype: list[str]
  """
  new_list = []
  for index in xrange(0, len(label_list)):
    value = label_list[index]
    random_value = random.randint(1, 10)
    if random_value < 2:
      new_list.append('neutral')
    else:
      new_list.append(value)
  return new_list


def calculate_kappa(filename):
  # save labels
  label_list = []
  with open('data/' + filename + '_data_result.json') as json_file:
    tweets = json.load(json_file)
    for row in tweets:
      label_list.append(row['label'])

  # Generate two fake labels to calculate kappa
  man_1_label = change_some_values(label_list)
  man_2_label = change_some_values(label_list)

  # save the labels to a csv file
  save_to_csv('data/label_1.csv', man_1_label)
  save_to_csv('data/label_2.csv', man_2_label)

  # calculate inter annotator agreement
  civ_1 = ['c1'] * len(man_1_label)
  civ_2 = ['c2'] * len(man_2_label)
  item_num_list = range(0, len(man_1_label))
  civ_1 = zip(civ_1, item_num_list, man_1_label)
  civ_2 = zip(civ_2, item_num_list, man_2_label)
  task_data = civ_1 + civ_2
  task = AnnotationTask(data=task_data)

  # observed disagreement for the weighted kappa coefficient
  print 'kappa: ' + str(task.kappa())


if __name__ == '__main__':
  calculate_kappa('espn')
