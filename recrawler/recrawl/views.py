from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from multiprocessing import Pool
import news_crawler
import json
import urllib2
import socket


def updateJSON(account):
  # crawl json from twitter
  print 'recrawling tweets from', account
  result_json = news_crawler.crawl(account)

  # send json file to SOLR server
  try:
    print 'updating solr server for', account 

    # You may change solr-node to localhost for development purpose. However, please do not check
    # that in, and keep the base url as solr-node:8983
    req = urllib2.Request(url='http://solr-node:8983/solr/sport/update/json?commit=true',
                          data=result_json)
    req.add_header('Content-type', 'application/json')
    response = urllib2.urlopen(req, timeout=2)
  except (socket.timeout, urllib2.URLError) as error:
    print error
    raise


@csrf_exempt
def recrawl(request):
  p = Pool(processes=2)
  res = p.apply_async(updateJSON, args=('espn',))
  res = p.apply_async(updateJSON, args=('TheNBACentral',))
  p.close()
  # p.join()
  return HttpResponse()
