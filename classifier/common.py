import csv
import os


def save_to_csv(filepath, data):
  with open(filepath, 'w') as label_file:
    wr = csv.writer(label_file, quoting=csv.QUOTE_ALL)
    wr.writerow(data)


def create_directory(data):
  try:
    os.makedirs(data)
  except OSError:
    if not os.path.isdir(data):
      raise
