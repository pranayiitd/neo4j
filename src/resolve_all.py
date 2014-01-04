from py2neo import neo4j
import json
from pprint import pprint
from datetime import datetime
import time
import os
import oauth2 as oauth
import twitter
import os
import sys


def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()

def insert_authors(loc, log, graph_db):
	# graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	batch = neo4j.WriteBatch(graph_db)
	BATCH_SIZE = 400

	f = open(loc,"r")
	line = f.readline()
	count =0
	while line:
		line = line.replace("\n", "")
		row = line.split("\t")
		uid = row[0]	
		# pro = json.loads(line)
		# profile = {
		# 			"uid" : pro['rtds_tweet']['user_id'],
		# 			"fo_c" : pro['rtds_tweet']['user_followers_count'],
		# 			"fr_c" : pro['rtds_tweet']['user_friends_count'],
		# 			"lang" : pro['rtds_tweet']['user_lang'],
		# 			"u_name" : pro['rtds_tweet']['user_name'],
		# 			"u_sc_name" : pro['rtds_tweet']['user_screen_name'],
		# 			"u_st_c" : pro['rtds_tweet']['user_statuses_count'],
		# 			"u_ver"  : pro['rtds_tweet']['user_verified'],
		# 			"u_utc" : pro['rtds_tweet']['user_utc_offset'],
		# 			"is_author" : '1'
		# 			}
		# batch.get_or_create_indexed_node("users", "uid",pro['rtds_tweet']['user_id'],profile)
		batch.get_or_create_indexed_node("users", "uid", uid, {"uid" : uid, "is_author" : '1'})
	


		count+=1
		if(count%BATCH_SIZE ==0):
			batch.submit()
			dump_log(log, [loc, datetime.now(), count])
		
		line = f.readline()
	batch.submit()
	dump_log(log, [loc, datetime.now(), count])
	f.close()

def insert_followers(uid, graph_db, client, version):
	# Getting data from twitter using API
	entry = twitter.get_followers(uid, 0, version, client)
	
	if(version==1):
		limit = int(entry['response']['x-ratelimit-remaining'])
	else:
		limit = int(entry['response']['x-rate-limit-remaining'])

	# Didn't get any followers.
	if(entry['followers'] == []):
		return [0, limit ]
	else:
		batch = neo4j.WriteBatch(graph_db)
		author = graph_db.get_indexed_node("users", "uid", str(uid))
		# this should be true as the authors profiles have been created first.
		if(author):
			followers = entry['followers']
			for fid in followers:
				batch.get_or_create_indexed_node("users","uid", fid ,{"uid" : fid,"is_author": "0"})
			nodes = batch.submit()
			# Create the relations
			for n in nodes:
				batch.get_or_create_relationship(n, "follows", author)
			rels = batch.submit()

		return [len(followers), limit]

def insert_friends(uid, graph_db, client, version):
	# Getting data from twitter using API
	entry = twitter.get_friends(uid, 0, version, client)
	
	if(version==1):
		limit = int(entry['response']['x-ratelimit-remaining'])
	else:
		limit = int(entry['response']['x-rate-limit-remaining'])

	# Didn't get any followers.
	if(entry['friends'] == []):
		return [0, limit ]
	else:
		batch = neo4j.WriteBatch(graph_db)
		author = graph_db.get_indexed_node("users", "uid", str(uid))
		# this should be true as the authors profiles have been created first.
		if(author):
			friends = entry['friends']
			for fid in friends:
				batch.get_or_create_indexed_node("users","uid", fid ,{"uid" : fid,"is_author": "0"})
			nodes = batch.submit()
			# Create the relations
			for n in nodes:
				batch.get_or_create_relationship(author, "follows", n)
			rels = batch.submit()

		return [len(friends), limit]




def main():
	fapp = open('twitter_app.txt',"r")
	lines = fapp.readlines()
	set_app =[]; i=0
	
	while (i+3)<(len(lines)):
		app = {}
		app['c_key'] = lines[i].replace("\n","")
		app['c_sec'] = lines[i+1].replace("\n","")
		app['a_key'] = lines[i+2].replace("\n","")
		app['a_sec'] = lines[i+3].replace("\n","")
		set_app.append(app)
		i+=5

	loc = "/home/pranayag/neo/cluster/sorted_tweets/1.txt"	
	log = "/home/pranayag/neo/logs/angelina_graph_log.txt"

	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

	# INSERT ALL THE AUTHORS NODE IN GRAPH DB
	# insert_authors(loc, log, graph_db)

	i = 0; v = 1; time_elapsed = 0
	count_followers = 0
	count_friends = 0
	count_authors = 0
	count_duplicats = 0
	limit = 4

	app = set_app[i]
	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)


	f = open(loc, "r")
	line = f.readline()
	while line:
	
		try:
			count_authors+=1
			line = line.replace("\n", "")
			row = line.split("\t")
			uid = row[0]	
			author_id = uid
			author = graph_db.get_indexed_node("users", "uid", str(author_id))

			if(author['resolved'] == None):
				count1, limit = insert_followers(author_id, graph_db, client, v)
				count2, limit = insert_friends(author_id, graph_db, client, v)
				author['resolved'] = 1
				count_followers += count1
				count_friends += count2
			else:
				count_duplicats +=1
				if(count_duplicats % 1000 == 0):
					dump_log(log, [loc, count_authors, count_followers, count_friends, datetime.now(), limit, count_duplicats,"passing_duplicates"])

			if(limit < 3):
				# Log the current status
				dump_log(log, [loc, count_authors, count_followers, count_friends, datetime.now(), limit,"limit_reached", i, v, time_elapsed ])
				i, v, time_elapsed = switch_sleep(i, v, time_elapsed, log, graph_db, author_id)
				app = set_app[i]
				CONSUMER_KEY = app['c_key']
				CONSUMER_SECRET = app['c_sec']
				ACCESS_KEY = app['a_key']
				ACCESS_SECRET = app['a_sec']
				consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
				access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
				client = oauth.Client(consumer, access_token)
		except:
			line = f.readline()
			dump_log(log, [loc, count_authors, count_followers, count_friends, datetime.now(), limit, sys.exc_info()[0]])
			continue
		
		line = f.readline()

	dump_log(log, [loc, count_authors, count_followers, count_friends, datetime.now(), limit,"end_while"])


def switch_sleep(i, v, time_elapsed, log, graph_db, author_id):
	time.sleep(1)
	if(i<3):
		i+=1
	else:
		if(v==1):
			v=1.1
			i=0
		else:
			dump_log(log, [ i, v, time_elapsed,  datetime.now(), "sleeping 15 mins"])
			for j in range(60):
				time.sleep(15)
				n = graph_db.get_indexed_node("users", "uid", str(author_id))
			time_elapsed +=15
			i=0
			if(time_elapsed >= 60):
				v=1
				time_elapsed=0	
	
	return [i, v, time_elapsed]

main()	
