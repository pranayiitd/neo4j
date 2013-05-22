# Get all the user profiles available in the tweets in RTDS and insert
# in the neo4j Database

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

# UPDATE THE NODE N WITH PROFILE EXTRACTED FROM TWEET OBJECT TOBJ
def update_profile(n, tobj):
		
	n["fo_c"] = tobj['rtds_tweet']['user_followers_count']
	n["fr_c"] = tobj['rtds_tweet']['user_friends_count']
	n["lang"] = tobj['rtds_tweet']['user_lang']
	n["u_name"] = tobj['rtds_tweet']['user_name']
	n["u_sc_name"] = tobj['rtds_tweet']['user_screen_name']
	n["u_st_c"] = tobj['rtds_tweet']['user_statuses_count']
	n["u_ver"]  = tobj['rtds_tweet']['user_verified']
	n["u_utc"] = tobj['rtds_tweet']['user_utc_offset']
	n["time_zone"] = tobj['rtds_tweet']['user_time_zone']





# Source of rtds twitter feeds.
# Source of rtds twitter feeds.
#loc = "/home/y/var/timesense/data/twitter_rawTweets/en-US/syc/2013-05-02/"


def main(loc, log):
	
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	count =0
	c1 =0; c2=0;c3=0

	f_list = os.listdir(loc)
	for f in f_list:
		fo = open(loc+f,"r")
		line = fo.readline()
		while line:
			c1+=1
			tobj = json.loads(line)
			# Check if that uid in DB.
			id_ = str(tobj['rtds_tweet']['user_id'])
			n = graph_db.get_indexed_node("users", "uid", id_)
			
			# update profile only if user in out database.
			# Activity reflects the frequent tweets by user.
			if(n):
				c2+=1
				if(n['activity']==None):
					n['activity']==1
				else:
					n['activity']+=1

				if(n['is_author']=='0' and n['activity'] == None):
					count+=1
					try:
						update_profile(n, tobj)

					except:
						line = fo.readline()
						c3+=1
						continue

				if(count %1000 == 0):
					dump_log(log, [f, datetime.now(), c1, c2, count, c3 ])
			
			line = fo.readline()		

		fo.close()

loc = "/home/y/var/timesense/data/twitter_filteredTweets_rsync/en-US/syc/2013-05-20/"
log = "/home/pranayag/neo/logs/profile_log_3.txt"
main(loc, log)

