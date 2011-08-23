from models import *
from twython import Twython

twitter = Twython()

def query_twitter(query_terms, page=1):
	term = add_term(query_terms)
	query = twitter.searchTwitter(geocode="37.62,-122.38,15mi",q=query_terms,rpp='100',page=str(page))
	for tweet in query['results']:
		tweet = add_tweet(tweet)
		term.tweets.append(tweet)
	db.session.commit()