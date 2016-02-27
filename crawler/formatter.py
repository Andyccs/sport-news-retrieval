import json
import codecs

FOLDER_NAME = 'crawler/'
DATA_FILE = 'espn_data'
RESULT_FILE = 'espn_data_result'
APPENDED_FILE = DATA_FILE + '_result_appended'
FILE_TYPE = '.json'
RESULT_KEY = "label"

def add_col(data_file, result_list, column_name):
  """
  add new column of result to data file.
  :param data_file: list of dict
  :param result_list: list
  :param column_name: list
  :return: list of dict
  """
  for data_file_row in data_file:
    for result in result_list:
      data_file_row[column_name] = result
  return data_file

# get all results into a list
result_list = []
with open(FOLDER_NAME + RESULT_FILE + FILE_TYPE, 'r') as result_file:
  result_json = json.load(result_file)
  for row in result_json:
    result_list.append(row[RESULT_KEY])

# add new column to the data file, creates a new file
with open(FOLDER_NAME + DATA_FILE + FILE_TYPE, 'r') as data_file, \
    codecs.open(FOLDER_NAME + APPENDED_FILE + FILE_TYPE, 'a+') as appended_file:
  data_json = json.load(data_file)
  appended_list = add_col(data_json, result_list, RESULT_KEY)
  # create new file for appended data and result
  json.dump(appended_list, appended_file)
