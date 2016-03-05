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
The recrawler will be served as a backend Django server and rely on the crawler to do the recrawling task for incremental index. When user submits a request to the server, it will perform an asynchronous task to crawl the tweets and upload the json file to Solr server.

1. Create a file `tweeter_key.py` in `recrawler\cz4034\recrawl` folder as shown in Crawler section. 
2. Navigate to `recrawler\cz4034` and run the localhost by using the following command:
```Shell
$ python manage.py runserver
```

To test it, simply submit a POST request to `http://127.0.0.1:8000/recrawl/` using javascript. It will return a HTTP reponse immediately and trigger the backend task.

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

Two json files, `espn_data_sentiments.json` and `TheNBACentral_data_sentiments.json`, will be created at the 'data' directory of this project. A new 'label' field is created for each tweet, with 3 possible values, i.e. 'neg', 'neutral', and 'pos'. 

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
$ export VERSION=v1.1-rc4
$ docker build -t asia.gcr.io/${PROJECT_ID}/proxy:${VERSION} --file proxy/Dockerfile .
$ docker build -t asia.gcr.io/${PROJECT_ID}/solr:${VERSION} --file index/Dockerfile .

$ gcloud docker push asia.gcr.io/${PROJECT_ID}/proxy:${VERSION}
$ gcloud docker push asia.gcr.io/${PROJECT_ID}/solr:${VERSION}
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

$ kubectl create -f kubernete/proxy-rc.yml
$ kubectl create -f kubernete/solr-rc.yml
```

Allow external traffic

```Shell
$ kubectl create -f kubernete/proxy-service.yml
$ kubectl create -f kubernete/solr-service.yml
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

$ kubectl delete rc proxy-node
$ kubectl delete rc solr-node
```

