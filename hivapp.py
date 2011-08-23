from flask import Flask, request, render_template, jsonify
from flaskext.sqlalchemy import SQLAlchemy
import re
import time
from datetime import datetime

from twython import Twython

from db_config import db_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
	return render_template('index.html')
	
@app.route('/tweets',methods=['GET','POST'])
def get_tweets():
	tweets = []
	total = 0
	if request.method == "POST" and 'day' in request.form and 'month'in request.form and 'year' in request.form:
		month = str(request.form['month'])
		if len(month)<2:
			month = "0"+month
		date_string = request.form['day']+"/"+month+"/"+request.form['year']
		print date_string
		tweets = Tweet.query.filter("strftime('%d/%m/%Y',posted) = :date").params(date=date_string).all()
		total = len(tweets)
	return jsonify(total = total)