#Bottle Framework
from bottle import route, run, template, request, static_file, get, post, request, Bottle, error
import bottle
import os

MONGOLAB_URI = os.environ['MONGOLAB_URI']

#specifying the path for the files
@route('/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='.')

@route("/")
def mynext():
	return template('index.html')

@route("/events")
def events():
	return template('events.html')

@route("/sessions")
def sessions():
	return template('sessions.html')

@route("/schedule")
def schedule():
	return template('schedule.html')

@route("/tweet")
def tweet():

	from TwitterAPI import TwitterAPI

	consumer_key = "TnVqAoTg0uLmT1vekmbXyjBu6"
	consumer_secret = "T6xavyxWaSoPcMNEeit0Hi4aiPz0nBPIU4LMTGUT4nap0qcV1M"
	access_token_key = "15196460-kLyCzkUjP6K0MPAH7u8mKNe70MDP0LSPNdOIsbqm5"
	access_token_secret = "3wjO9iveywpKLm0AX9bi2Ry4XJEONgWNOb1MXDfRZPPeg"

	api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

	r = api.request('statuses/user_timeline', {'screen_name':'mynextofficial','exclude_replies':'true'})

	tweet_list = []

	for item in r:
		tweet_list.append([item['user']['screen_name'],item['text'],item['id']])


	return template('twitter.html', tweet_list=tweet_list)

import pymongo
from pymongo import MongoClient

@route("/register", "GET")
def register():
	getName = request.query.InputName
	getEmail = request.query.InputEmail
	getUni = request.query.InputUni
	client = MongoClient(MONGOLAB_URI)
	db = client.get_default_database()
	users = db['users']

	if getEmail:
		users.insert({"name":str(getName),"email":str(getEmail),"university":str(getUni)})
		return template('register.html',registered=True)

	return template('register.html', registered=False)

@route("/resources")
def resources():
	getName = request.query.InputName
	getEmail = request.query.InputEmail
	getUni = request.query.InputUni
	client = MongoClient(MONGOLAB_URI)
	db = client.get_default_database()
	resources = db['resources']
	cursor = resources.find()
	links = list(cursor)
	return template('resources.html',links=links)

# Route to support page
@route("/support")
def support():
	return template('support.html')

# Route to about page
@route("/about")
def about():
	return template('about.html')

# @route('/favicon.ico')
# def get_favicon():
# 	return server_static('favicon.ico')

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

