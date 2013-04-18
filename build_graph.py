from py2neo import neo4j
import json
from pprint import pprint

def insert_authors(loc):
	
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	batch = neo4j.WriteBatch(graph_db)
	BATCH_SIZE = 400

	f = open(loc,"r")
	line = f.readline()
	print "Starting....."
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

l = "/Users/pranayag/mtp/visualize/data/authors.txt"	
insert_authors(l)