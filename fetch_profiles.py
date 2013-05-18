from py2neo import neo4j
import json
from pprint import pprint
from datetime import datetime
import os

def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()


def update_profile(n, tobj):
		
	n["fo_c"] = tobj['user_followers_count']
	n["fr_c"] = tobj['user_friends_count']
	n["lang"] = tobj['user_lang']
	n["u_name"] = tobj['user_name']
	n["u_sc_name"] = tobj['user_screen_name']
	n["u_st_c"] = tobj['user_statuses_count']
	n["u_ver"]  = tobj['user_verified']
	n["u_utc"] = tobj['user_utc_offset']
	# n["is_author"] = '1'






graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

loc = "/home/y/var/timesense/data/twitter_rawTweets/en-US/syc/2013-05-02/"
log = "/home/pranayag/neo/src/profile_log.txt"

fl = os.listdir(loc)
for f in fl:
	fo = open(loc+f,"r")
	line = fo.readline()
	count =0	
	while line:
		
		tobj = json.loads(line)
		pprint(tobj)
		# Check if that uid in DB.
		id_ = str(tobj['rtds_tweet']['user_id'])
		n = graph_db.get_indexed_node("users", "uid", id_)
		
		if(n):
			if(n['activity']==None):
				n['activity']==1
			else:
				n['activity']+=1

			if(n['is_author']=='0' and n['activity'] == None):
				update_profile(n, tobj)
				count+=1

			if(count %100==0):
				dump_log(log, [loc+f, datetime.now(), count ])
		
		line = fo.readline()		

	fo.close()
