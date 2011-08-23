from flask import Flask, request, render_template, jsonify
from flaskext.sqlalchemy import SQLAlchemy
import re

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
	total = 0
	if request.method == "POST" and 'region' in request.form and 'types' in request.form:
		total = 10
	return jsonify(total = total)