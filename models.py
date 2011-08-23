from hivapp import db
import time
from datetime import datetime

def add_tweet(data):
	tweet = Tweet.query.filter_by(tweet_id=data['id_str']).first()
	if tweet is None and 'created_at' in data:
		d = time.strptime(data['created_at'][0:len(data['created_at'])-6],'%a, %d %b %Y %H:%M:%S')
		data['created_at'] = datetime.fromtimestamp(time.mktime(d))
		
		tweet = Tweet(data['id_str'],data['from_user'],data['text'],data['created_at'])
		if 'location' in data and data['location'] is not None:
			tweet.location = data['location']
		if data['geo'] is not None and data['geo']['coordinates'] is not None and len(data['geo']['coordinates'])>1:
			tweet.lat = data['geo']['coordinates'][0]
			tweet.lng = data['geo']['coordinates'][1]
		db.session.add(tweet)
		db.session.commit()
	return tweet
	
def add_term(query_string):
	term = Term.query.filter_by(text=query_string).first()
	if term is None:
		term = Term(query_string)
		db.session.add(term)
		db.session.commit()
	return term

tweets_to_terms = db.Table('tweets_to_queries',
	db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.id')),
	db.Column('term_id', db.Integer, db.ForeignKey('term.id'))
	)

class Tweet(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	tweet_id = db.Column(db.String(200))
	user = db.Column(db.String(25))
	text = db.Column(db.String(200))
	location = db.Column(db.String(255))
	lat = db.Column(db.Float,nullable=True)
	lng = db.Column(db.Float,nullable=True)
	posted = db.Column(db.DateTime)
	hidden = db.Column(db.Boolean)
	terms = db.relationship('Term' ,secondary=tweets_to_terms, backref=db.backref('source',lazy='dynamic'))
	
	def __init__(self, tweet_id, user, text, posted):
		self.tweet_id = tweet_id
		self.user = user
		self.text = text
		self.posted = posted
		self.hidden = False
	
class Term(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(100))
	tweets = db.relationship('Tweet' ,secondary=tweets_to_terms, backref=db.backref('source',lazy='dynamic'))
	
	def __init__(self, text):
		self.text = text
	
	def __repr__(self):
		return '<Term %r>' % self.text