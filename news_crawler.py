import tweepy

consumer_key = 'Your-key-here'
consumer_secret = 'Your-key-here'
access_token = 'Your-key-here'
access_token_secret = 'Your-key-here'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for i in range(1,51):
  tweets = api.user_timeline('espn', count=200, page=i)
  print 'page', i, 'count', len(tweets)
  # for tweet in tweets:
  #   print tweet.text
  #   print '========================='

# espn has 200 data in the first 16 page, and 1 data in 17 page
