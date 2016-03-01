#!/bin/bash -e
GREEN='\033[0;32m'
NC='\033[0m'

function d_cleanup() {
  docker ps -aqf status=exited | xargs docker rm
  docker images -qf dangling=true | xargs docker rmi
}

function crawl_news() {
  printf "${GREEN}Recrawing${NC}\n"
  python crawler/news_crawler.py
}

function sentiment_analysis() {
  printf "${GREEN}Classifying${NC}\n"
  python classifier/classify.py
}

function sportd() {
  if [ "$1" != "start" ]
  then
    echo "Usage: sportd start [OPTION]"
    echo "Options: "
    echo "-c     crawl data before start"
    echo "-cc    crawl and classify data before start"
    return
  fi

  printf "${GREEN}Installing all requirements${NC}\n"
  pip install -r requirement.txt

  if [ "$2" == "-c" ]
  then
    crawl_news
  fi

  if [ "$2" == "-cc" ]
  then
    crawl_news
    sentiment_analysis
    rm data/*_data.json
  fi
  
  printf "${GREEN}Installing bower components${NC}\n"
  cd UI && bower install && cd ../

  printf "${GREEN}Cleanup unused images and containers${NC}\n"
  d_cleanup

  printf "${GREEN}Starting Solr Server and wait 3 seconds${NC}\n"
  docker-compose up -d
  sleep 3

  printf "${GREEN}Indexing data${NC}\n"
  docker exec sportnewsretrieval_solr_1 bin/post -c sport data/*.json  
}
