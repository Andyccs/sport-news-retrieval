#!/bin/bash -e
function d_cleanup() {
  docker ps -aqf status=exited | xargs docker rm
  docker images -qf dangling=true | xargs docker rmi
}

GREEN='\033[0;32m'
NC='\033[0m'

printf "${GREEN}Installing all requirements${NC}\n"
pip install -r requirement.txt

if [ "$1" == "-c" ]
then
  printf "${GREEN}Recrawing${NC}\n"
  python crawler/news_crawler.py
fi

if [ "$1" == "-cc" ]
then
  printf "${GREEN}Recrawing${NC}\n"
  python crawler/news_crawler.py

  printf "${GREEN}Classifying${NC}\n"
  python classifier/classify.py

  rm data/*_data.json
fi

printf "${GREEN}Cleanup unused images and containers${NC}\n"
d_cleanup

printf "${GREEN}Starting Solr Server and wait 3 seconds${NC}\n"
docker-compose up -d
sleep 3

printf "${GREEN}Indexing data${NC}\n"
docker exec sportnewsretrieval_solr_1 bin/post -c sport data/*.json
