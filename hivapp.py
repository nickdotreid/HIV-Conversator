from flask import Flask, request, render_template, jsonify
from flaskext.sqlalchemy import SQLAlchemy
import re

from twython import Twython

from db_config import db_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

from models import *