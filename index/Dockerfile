# You must be in the root directory of this project when building this image
FROM solr:5.5

USER root

COPY data/all_data.json /opt/solr/data/all_data.json
COPY index/solr/sport/core.properties /tmp/solr/sport/core.properties
COPY index/solr/sport/conf /tmp/solr/sport/conf
COPY index/solr/solr.xml /tmp/solr/solr.xml
CMD ["/opt/solr/bin/solr", "start", "-f", "-s", "/tmp/solr/"]
