from models import *
from twython import Twython

twitter = Twython()

def query_twitter(query_terms):
	query = twitter.searchTwitter(geocode="37.62,-122.38,15mi",q=query_terms)
	for tweet in query['results']:
		add_tweet(tweet)