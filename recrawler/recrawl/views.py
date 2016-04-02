from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from multiprocessing import Pool
import threading
import news_crawler
import sys
sys.path.insert(0, '../classifier')
import classify_data
import json
import urllib2
import socket


def crawl_data(account):
  # crawl json from twitter
  print 'recrawling tweets from', account
  news_crawler.crawl(account)


def update_solr():
  json_data = open('../data/all_data.json')
  temp = json.load(json_data)
  result_json = json.dumps(temp)

  # send json file to SOLR server
  try:
    print 'updating solr server'

    # You may change solr-node to localhost for development purpose. However, please do not check
    # that in, and keep the base url as solr-node:8983
    req = urllib2.Request(url='http://solr-node:8983/solr/sport/update/json?commit=true',
                          data=result_json)
    req.add_header('Content-type', 'application/json')
    response = urllib2.urlopen(req)
  except (socket.timeout, urllib2.URLError) as error:
    print error
    raise


def background_process():
  # crawl data
  p = Pool(processes=5)
  res = p.apply_async(crawl_data, args=('espn',))
  res = p.apply_async(crawl_data, args=('TheNBACentral',))
  res = p.apply_async(crawl_data, args=('SimpleNBAScores',))
  res = p.apply_async(crawl_data, args=('ESPNNBA',))
  res = p.apply_async(crawl_data, args=('NBATV',))
  p.close()
  p.join()
  print "Finish crawling"

  # classify data
  classify_data.classify_data()
  print "Finish classifying"

  # update solr server
  update_solr()
  print "Finish updating"


@csrf_exempt
def recrawl(request):
  t = threading.Thread(target=background_process)
  # Want the program to wait on this thread before shutting down.
  t.setDaemon(False)
  t.start()

  return HttpResponse()
