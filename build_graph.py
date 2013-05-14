# This scripts generates the neo4j graph from the social relations
# extracted using TwitterAPI and stored in text json objects



from py2neo import neo4j
import json
from pprint import pprint
from datetime import datetime

def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()

def insert_authors(loc):
	
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	batch = neo4j.WriteBatch(graph_db)
	BATCH_SIZE = 400

	f = open(loc,"r")
	line = f.readline()
	count =0
	while line:
		pro = json.loads(line)
		profile = {
					"uid" : pro['user_id'],
					"fo_c" : pro['user_followers_count'],
					"fr_c" : pro['user_friends_count'],
					"lang" : pro['user_lang'],
					"u_name" : pro['user_name'],
					"u_sc_name" : pro['user_screen_name'],
					"u_st_c" : pro['user_statuses_count'],
					"u_ver"  : pro['user_verified'],
					"u_utc" : pro['user_utc_offset'],
					"is_author" : '1'
					}
		batch.get_or_create_indexed_node("users", "uid",pro['user_id'],profile)
		count+=1
		if(count==BATCH_SIZE):
			count =0
			batch.submit()
			# batch.clear()
			print "A batch inserted."
		
		line = f.readline()

	f.close()

def insert_followers(loc):
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	batch = neo4j.WriteBatch(graph_db)
	BATCH_SIZE = 400

	f = open(loc,"r")
	line = f.readline()
	count =0
	while line:
		entry = json.loads(line)
		uid = entry['author']
		author = graph_db.get_indexed_node("users", "uid", str(uid))
		if(author):
			followers = entry['followers']
			for fid in followers:
				batch.get_or_create_indexed_node("users","uid", fid ,{"uid" : fid,"is_author": "0"})
			nodes = batch.submit()
			# Create the relations
			for n in nodes:
				batch.get_or_create_relationship(n, "follows", author)
			rels = batch.submit()
			cout+=1
			# print rels
			# print "A batch of relations inserted"
			dump_log("/home/pranayag/neo/src/graph_insert_log.txt", [loc, datetime.now(), count])
		else:
			# print "author not in db"
			dump_log("/home/pranayag/neo/src/graph_insert_log.txt", [loc, datetime.now(), -1])
		# print author
		# print graph_db.get_properties(author)
		# break
		line = f.readline()

	f.close()

def insert_friends(loc):
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	batch = neo4j.WriteBatch(graph_db)
	BATCH_SIZE = 400

	f = open(loc,"r")
	line = f.readline()
	count =0
	while line:
		entry = json.loads(line)
		uid = entry['author']
		# pprint(entry)
		# break
		author = graph_db.get_indexed_node("users", "uid", str(uid))
		if(author):
			friends = entry['friends']
			for fid in friends:
				batch.get_or_create_indexed_node("users","uid", fid ,{"uid" : fid,"is_author": "0"})
			nodes = batch.submit()
			
			# Create the relations
			for n in nodes:
				batch.get_or_create_relationship(author, "follows", n)
			
			rels = batch.submit()
			count+=1
			

			# print rels
			# print "inserted batch id ",count
			dump_log("/home/pranayag/neo/src/graph_insert_log.txt", [loc, datetime.now(), count])
		
		else:
			dump_log("/home/pranayag/neo/src/graph_insert_log.txt", [loc, datetime.now(), -1])
			# print "author not in db"
		# print author
		# print graph_db.get_properties(author)
		# break
		line = f.readline()
	f.close()


l1 = "/home/pranayag/graph/2013-04-03/authors.txt"
l2 = "/home/pranayag/graph/2013-04-03/followers.txt"
l3 = "/home/pranayag/graph/2013-04-03/friends.txt"

# insert_authors(l1)
#insert_followers(l2)
insert_friends(l3)