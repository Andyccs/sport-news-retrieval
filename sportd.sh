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

function install_python_requirements() {
  printf "${GREEN}Installing all requirements${NC}\n"
  pip install -r crawler/requirements.txt
  pip install -r classifier/requirements.txt
}

function sportd() {
  if [ "$1" "==" "stop" ]
  then
    printf "${GREEN}Stopping all...${NC}\n"
    docker-compose stop
    return
  fi

  if [ "$1" "!=" "start" ]
  then
    echo "Usage: sportd start [OPTION]"
    echo "Options: "
    echo "-c     crawl data before start"
    echo "-cc    crawl and classify data before start"
    return
  fi


  if [ "$2" "==" "-c" ]
  then
    install_python_requirements
    crawl_news
  fi

  if [ "$2" "==" "-cc" ]
  then
    install_python_requirements
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
  docker exec sportnewsretrieval_solr-node_1 bin/post -c sport data/all_data.json

  printf "${GREEN}If you get \"Connection error\" or \"Connection refuse\", please shout out the following numbers loudly:\n"
  printf "1 2 3 4 5\n"
  printf "and run the following command:\n"
  printf "docker exec sportnewsretrieval_solr-node_1 bin/post -c sport data/all_data.json${NC}\n"
}
