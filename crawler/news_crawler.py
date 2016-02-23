import datetime
import json
import tweepy
from tweeter_key import *


class Model:

  def __init__(self, text, author, datetime, lang, favorite_count):
    self.text = text
    self.author = author
    self.datetime = datetime
    self.lang = lang
    self.favorite_count = favorite_count


class ModelEncoder(json.JSONEncoder):

  def default(self, obj):
    if isinstance(obj, Model):
      return {"text": obj.text,
              "author": obj.author,
              "datetime": obj.datetime,
              "lang": obj.lang,
              "favorite_count": obj.favorite_count}
    # Let the base class default method raise the TypeError
    return json.JSONEncoder.default(self, obj)


epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
  return (dt - epoch).total_seconds() * 1000.0


def crawl(name, total_page):
  print 'crawling', name, 'tweeter timeline'

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  result = []
  api = tweepy.API(auth)

  for i in range(1, total_page + 1):
    print 'crawling page', i

    tweets = api.user_timeline(name, count=200, page=i)

    for tweet in tweets:
      text = tweet.text
      author = tweet.author.name
      created_at = tweet.created_at
      lang = tweet.lang
      favorite_count = tweet.favorite_count

      data = Model(text, author, unix_time_millis(created_at), lang, favorite_count)
      result.append(data)

    print 'crawled', len(tweets), 'tweets'

  result_json = json.dumps(result, cls=ModelEncoder)

  f = open(name + '_data.json', 'w')
  f.write(result_json)
  f.close()


if __name__ == "__main__":
  crawl('espn', 17)
  crawl('TheNBACentral', 17)
