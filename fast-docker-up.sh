#!/bin/bash -e
docker-compose up -d
sleep 3
docker exec sportnewsretrieval_solr_1 bin/post -c sport data/*.json
