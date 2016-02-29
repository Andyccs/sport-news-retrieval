# Sport News Retrieval

CZ4034 Information Retrieval Assignment

## Setting up

First, we install all requirements for this project by using the following command:

```Shell
$ pip install -r requirements.txt
```

## Crawler

The crawler will crawl [ESPN](https://twitter.com/espn?lang=en) and [TheNBACentral](https://twitter.com/TheNBACentral?lang=en) twitter timeline. To use this crawler, we first need to obtain an API key from [Twitter Application Management](https://apps.twitter.com) website. Next, create a file `tweeter_key.py` in `crawler` folder. This file will not be checked in to Git. 

```Python
# Replace the values with your API key values
consumer_key = 'Your key here'
consumer_secret = 'Your key here'
access_token = 'Your key here'
access_token_secret = 'Your key here'
```

We run the crawler by using the following command:

```Shell
$ python crawler/news_crawler.py
```

Two json files, `espn_data.json` and `The NBACentral_data.json`, will be created at the root directory of this project.

## Indexing

We start Solr 5 server and index our data by using the following commands:

```Shell
$ solr start -s root_of_project/index/solr
$ post -c sport espn_data.json
$ post -c sport TheNBACentral_data.json
```
## Classifier

The classifier will call the API from [text-processing.com](text-processing.com/api) 


We run the classifier by using the following command:

```Shell
$ python classifier/classify.py
```

A json files, `espn_data_result.json`  will be created at the root directory of this project. The json file has 4 fields: probability values of negative ('neg'), neutral ('neutral') and positive ('pos') and finally the sentiment label ('label') of the text.

After running the classifier, you may add the label to the data file by running formatter.py. 

```Shell
$ python crawler/formatter.py
```

A json file, `espn_data_result_appended.json` will be created. 