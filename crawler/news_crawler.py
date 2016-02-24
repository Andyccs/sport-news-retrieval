import datetime
import json
import pytz
import tweepy
from tweeter_key import *


class Model:

  def __init__(self, unique_id, text, author, created_at, lang, favorite_count):
    self.text = text
    self.author = author
    self.created_at = created_at
    self.lang = lang
    self.favorite_count = favorite_count
    self.unique_id = unique_id


class ModelEncoder(json.JSONEncoder):

  def default(self, obj):
    if isinstance(obj, Model):
      return {"id": obj.unique_id,
              "text": obj.text,
              "author": obj.author,
              "created_at": obj.created_at,
              "lang": obj.lang,
              "favorite_count": obj.favorite_count}
    # Let the base class default method raise the TypeError
    return json.JSONEncoder.default(self, obj)


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
      unique_id = tweet.id
      text = tweet.text
      author = tweet.author.name
      created_at = tweet.created_at.isoformat() + 'Z'
      lang = tweet.lang
      favorite_count = tweet.favorite_count

      data = Model(unique_id, text, author, created_at, lang, favorite_count)
      result.append(data)

    print 'crawled', len(tweets), 'tweets'

  result_json = json.dumps(result, cls=ModelEncoder)

  f = open(name + '_data.json', 'w')
  f.write(result_json)
  f.close()


if __name__ == "__main__":
  crawl('espn', 17)
  crawl('TheNBACentral', 17)
