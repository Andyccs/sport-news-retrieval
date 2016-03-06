from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from multiprocessing import Pool
import news_crawler
import json
import urllib2
import socket


def updateJSON():
  # crawl json from twitter
  result_json = news_crawler.crawl('espn', 1)
  
  # send json file to SOLR server
  try:
    req = urllib2.Request(url='http://localhost:8983/solr/sport/update/json?commit=true',
                          data=result_json)
    req.add_header('Content-type', 'application/json')
    response = urllib2.urlopen(req, timeout=2)
  except (socket.timeout, urllib2.URLError) as error:
    print error
    raise


@csrf_exempt
def recrawl(request):
  print 'recrawling tweets'
  p = Pool(processes=1)
  result = p.apply_async(updateJSON)
  return HttpResponse()
