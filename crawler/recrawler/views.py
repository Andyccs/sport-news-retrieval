from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from multiprocessing import Pool
import news_crawler
import json
import urllib2
import socket

class MyException(Exception):
	pass

def updateJSON():
	# crawl json from twitter
	result_json = news_crawler.crawl('espn', 1)
	print result_json

	# send json file to SOLR server
	try:
		req = urllib2.Request(url='http://localhost:8983/solr/update/json?commit=true', data=result_json)
		req.add_header('Content-type', 'application/json')
		response = urllib2.urlopen(req, timeout=2)
	except urllib2.URLError, e:
		print type(e)
		raise MyException("Error: %r" % e)
	except socket.timeout, e:
		print type(e)
		raise MyException("Error: %r" % e)

@csrf_exempt
def recrawl(request):
	print "BEGIN"
	p = Pool(processes=1)
	result = p.apply_async(updateJSON)
	return HttpResponse("Recrawling")