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

*Note: In the current implementation, an alert view will show up once the button is clicked. In the future, we shall modify the clicking event so that it makes the recrawling request to backend.*

*Note: In the current implementation, a HTTP GET request is made to UI/fake_news.json and display the records in that file. In the future, we need to query the backend solr and we shall also edit the html template based on its schema.*

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

First, we need to make sure that your Docker client is connected to your Docker daemon. 

```Shell
# Only Mac OSX can run the following command.
$ docker-machine start
$ docker-machine env default
$ eval $(docker-machine env default) 

# For Windows users, please copy paste the output of previous command to your
# command line. 
$ docker-machine start
$ docker-machine env default

# For Linux
# Make sure you can run docker without sudo by [creating a docker group](https://docs.docker.com/engine/installation/linux/ubuntulinux/#create-a-docker-group)
$ sudo service docker start
```

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
