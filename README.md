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

Two json files, `espn_data.json` and `TheNBACentral_data.json`, will be created at the root directory of this project.

## Indexing

We start Solr 5.0 server and index our data by using the following commands:

```Shell
$ solr start -s root_of_project/index/solr
$ post -c sport espn_data.json
$ post -c sport TheNBACentral_data.json
```
## Classifier

The classifier will call the API from [text-processing.com](text-processing.com/api). We run the classifier by using the following command:

```Shell
$ python classifier/classify.py
```

Two json files, `espn_data_sentiments.json` and `TheNBACentral_data_sentiments.json`, will be created at the root directory of this project. A new 'label' field is created for each tweet, with 3 possible values, i.e. 'neg', 'neutral', and 'pos'. 

## UI Client
Current UI version has two functions:

- A button to trigger the crawling in the backend
- A text area waiting for keywords. The click of search button will trigger a query to backend solr to retrieve records. Then records are displayed in the page. 

*Note: In the current implementation, an alert view will show up once the button is clicked. In the future, we shall modify the clicking event so that it makes the recrawling request to backend.*

*Note: In the current implementation, a HTTP GET request is made to UI/fake_news.json and display the records in that file. In the future, we need to query the backend solr and we shall also edit the html template based on its schema.*
