import urllib
import json
import codecs

FILE_NAME = 'espn_data'

with open('crawler/' + FILE_NAME + '.json') as json_file:
    data_json = json.load(json_file)

# do sentiment analysis
result_list = []
for tweet_data in data_json:
    text = tweet_data['text'].encode('ascii', 'ignore')
    data = urllib.urlencode({"text": text})
    result = urllib.urlopen("http://text-processing.com/api/sentiment/", data)
    result_list.append(result.read())

# save result
with codecs.open('crawler/' + FILE_NAME + '_result.json', 'a+') as result_file:
    json.dump(result_list, result_file)

