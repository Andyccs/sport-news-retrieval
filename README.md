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

Two json files, `espn_data.json` and `TheNBACentral_data.json`, will be created at the `data` directory of this project.

## Recrawler

The recrawler is a Django server and rely on the crawler to do the recrawling task for incremental index. When user submits a request to the server, it will perform an asynchronous task to crawl the tweets and send an update request to Solr server. To run the recrawler server, we first need to setup the crawler, as mentioned in previous section. Then, we run the following commands:

```Shell
$ cd recrawler
$ python manage.py migrate
$ python manage.py runserver
```

To test the recrawler, we just need to submit a GET/POST request to `http://localhost:8000/recrawler-service/recrawl`. The recrawler will return a 200 HTTP reponse immediately and crawling the first 200 tweets from selected accounts asynchronously.

## Indexing

We start Solr 5.0 server and index our data by using the following commands:

```Shell
$ solr start -s root_of_project/index/solr
$ post -c sport espn_data.json
$ post -c sport TheNBACentral_data.json
```
## Classifier

You need to run the crawler at least once, and make sure that `espn_data.json` file is available in data folder. The pipeline of our classifier is shown in the figure below

```
espn_data.json --> classify.py --> preprocess.py --> some classifier --> evaluation_metrics.py
```

We will first call the API from [text-processing.com](text-processing.com/api) to label our raw data. The following script will call the API, an output a json file `espn_data_result.json` in `data` folder. `espn_data_result.json` contains probabilities and labels for data. The API only allows 1 request per seconds, so you might want to grab a coffee while waiting.

```Shell
$ python classifier/classify.py

# Example content of espn_data_result.json
# [{
#   "probability": {
#     "neg": 0.4768910438883407,
#     "neutral": 0.8121072206192833,
#     "pos": 0.5231089561116593
#   },
#   "label": "neutral"
# }]
```

Next, we need to run the preprocessing step. The preprocessing step will do the following in sequence:

1. Lower case
2. remove html
3. remove stopwords

Then, it will output the preprocessed data to `labelled_tweets.csv`. We can run the preprocess step by using the following script:

```Shell
$ python classifier/preprocess.py

# Example content of labelled_tweets.csv
# "buzzer-beating 3 win crucial bubble game make gary payton happy? #pac12afterdark never disappoints. https://t.co/hh0omzffa8","diaz: you're steroids mcgregor: sure am. i'm animal. icymi: #ufc196 presser went expected. https://t.co/jqb72ohv4g"
```

**The preprocess.py will also do a fake inter-annotator agreement calculation. Specifically, it will slightly change the labels espn_data_result.json to calculate kappa. This is cheating.**

After preprocessing step, we will run train some classifiers and evaluate the classifier. Currently, we have three classifier, i.e. linear support vector classification, gensim classifier, and ensemble classifier. By default, the following scriptsw ill use `evaluation_metrics.py` to generate evalutation metrics. 

```Shell
# linear support vector classification
# output:
# - data/log_reg_result.csv
# - figure/tfid_linsvc_classifier
# - metric_result/tfid_linsvc_classifier.txt
# - model/linear_svc.pkl*
$ python classifier/linear_svc.py

# gensim classifier
# output:
# - data/word2vec_linsvc_result.csv
# - figure/gensim_classifier
# - metric_result/gensim_classifier.txt
# - model/word2vec_model.doc2vec
$ python classifier/gensim_classifier.py

# ensemble classifier
# output:
# - data/ensemble_ada_result.csv
# - metric/ensemble_ada.txt
# - model/ensemble_ada_classifier.pickle
$ python classifier/ensemble_classifier.py 
```

## Check Model Time

TODO(kklw)

```Shell
# output: metric_result/timings.txt
$ python classifier/check_model_time.py
```

## Run all commands in one script

To run all the above commands:

```Shell
$ python classifier/main.py
```

### Inter annotator agreement
The preprocessing.py class calls the nltk [annotation task][https://github.com/tousif/nltk-gae/blob/master/nltk/metrics/agreement.py].

## UI Client

We have a simple user interface that use Solr server to retrieve sport news. Current UI version has two functions:

- A button to trigger the crawling in the backend
- A text area waiting for keywords. The click of search button will trigger a query to backend solr to retrieve records. Then records are displayed in the page. 

*Note: In the current implementation, an alert view will show up once the button is clicked. In the future, we shall modify the clicking event so that it makes the recrawling request to backend. TODO(RUAN0007): we need a backend server to accomplish recrawling task*

To install all components for this website, we first need to install bower using [node package manager](https://www.npmjs.com/):

```Shell
$ npm install -g bower
```

Then we install all dependencies using bower:

```Shell
$ cd UI
$ bower install
```

You can open the `UI/index.html` file to view the simple website. Please take note that some functionality may not work if you didn't run Solr server and serve static content from the same domain.

## But wait, there are so many things I need to do to run the simple website!

Yeah you are right. You need to install all Python requirements, install all bower components, crawl data, classifier data, host static files using some kind of server, run solr server and index data using solr. Tedious right? Let's magic happens!

Prerequisite:

- Mac OSX or Unix
  - Windows user can use Git Bash or [Cygwin](https://www.cygwin.com))
- [Docker Toolbox](https://www.docker.com/products/docker-toolbox) is installed
  - For Linux users, you should install [Docker Engine](https://docs.docker.com/linux/) and [Docker Compose](https://docs.docker.com/compose/install/) separately
- Python 2 or 3 and Python Package Manager (pip) is installed
- [Bower](http://bower.io) is installed
- Windows users must make sure that these programs are added to the PATH environment variables and can be run using command line
- You have create a file `crawler/tweeter_key.py` by following the guide in `Crawler` section of this README

First, we need to make sure that your Docker client is connected to your Docker daemon. 

```Shell
# Only Mac OSX can run the following command.
$ docker-machine start default
$ docker-machine env default
$ eval $(docker-machine env default)

# For Windows users, please copy paste the output of previous command to your
# command line. 
$ docker-machine start default
$ docker-machine env default

# For Linux
# Make sure you can run docker without sudo by creating a docker group
$ sudo service docker start
```

*[Creating a docker group in Linux](https://docs.docker.com/engine/installation/linux/ubuntulinux/#create-a-docker-group)*

Alternatively, Mac OSX and Windows users can connect to Docker daemon using `Docker Quickstart Terminal` program. 

Next, we run all these tedious steps using the following commands:

```Shell
$ source sportd.sh

# If you want to crawl, classify, start solr server and website
$ sportd start -cc

# If you do not want to classify, and only want to crawl, start solr server and website
$ sportd start -c

# If you do not want to crawl and classify, and only want to start solr server and website
$ sportd start

# You should only use sportd command in the root directory of this project
```

After running the commands, the application will be deployed to a virtual machine. We need to know the ip address of our virtual machine using the following commands:

```Shell
# For MAC OSX and Windosw
$ docker-machine ip default

# For Linux
$ ifconfig docker0 | grep 'inet addr:' | cut -d: -f2 |  cut -d ' ' -f 1
```

Now, you can visit the website at `http://theipaddress` and the Solr Admin Panel at `http://theipaddress:8983`.

To stop the magic from happening:

```Shell
$ sportd stop
```

## Deploy to Google Container Engine

Build docker images:

```Shell
$ export PROJECT_ID=sport-news-retrieval
$ export VERSION=v1.1-rc5
$ docker build -t asia.gcr.io/${PROJECT_ID}/proxy:${VERSION} --file proxy/Dockerfile .
$ docker build -t asia.gcr.io/${PROJECT_ID}/solr:${VERSION} --file index/Dockerfile .
$ docker build -t asia.gcr.io/${PROJECT_ID}/recrawler:${VERSION} --file recrawler/Dockerfile .

$ gcloud docker push asia.gcr.io/${PROJECT_ID}/proxy:${VERSION}
$ gcloud docker push asia.gcr.io/${PROJECT_ID}/solr:${VERSION}
$ gcloud docker push asia.gcr.io/${PROJECT_ID}/recrawler:${VERSION}
```

Create cluster:

```Shell
# Only do the following for once
$ gcloud container clusters create sport-news-retrieval \
    --num-nodes 1 \
    --machine-type g1-small

# Check the newly created instances
$ gcloud compute instances list
```

Create your pods:

```Shell
# Config gcloud and kubectl, only do the following for once
$ gcloud config set project sport-news-retrieval
$ gcloud config set compute/zone asia-east1-a
$ gcloud config set container/cluster sport-news-retrieval
$ gcloud container clusters get-credentials sport-news-retrieval

# If you want to create new replication controller (typically for first time users)
$ kubectl create -f kubernete/proxy-rc.yml
$ kubectl create -f kubernete/solr-rc.yml
$ kubectl create -f kubernete/recrawler-rc.yml

# If you just want to update images
$ kubectl rolling-update proxy-node --image=asia.gcr.io/${PROJECT_ID}/proxy:${VERSION}
$ kubectl rolling-update solr-node --image=asia.gcr.io/${PROJECT_ID}/solr:${VERSION}
$ kubectl rolling-update recrawler-node --image=asia.gcr.io/${PROJECT_ID}/recrawler:${VERSION}
```

Allow external traffic

```Shell
$ kubectl create -f kubernete/proxy-service.yml
$ kubectl create -f kubernete/solr-service.yml
$ kubectl create -f kubernete/recrawler-service.yml
```

View Status:

```Shell
$ kubectl get pods
$ kubectl get services
```

Indexing to solr:
```Shell
$ bin/post -c sport -host <external ip of solr-node> data/*.json
```

Stop all pods and services:

```Shell
$ kubectl delete services solr-node
$ kubectl delete services proxy-node
$ kubectl delete services recrawler-node

$ kubectl delete rc proxy-node
$ kubectl delete rc solr-node
$ kubectl delete services recrawler-node
```

