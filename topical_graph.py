# For a given topic it will make anothe neo4j instance for topical graph of the
# given topic. 
# Then making it evolving graph.

from py2neo import neo4j
import json
from pprint import pprint
from datetime import datetime
import connected_comp

def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()




def insert_day_1(loc):
	
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	graph_db_topic = neo4j.GraphDatabaseService("http://localhost:7475/db/data/")
	
	f = open(loc,"r")
	line = f.readline()
	c1 =0
	c2 =0
	while(line):
		c1+=1
		tobj = json.loads(line)
		id_ = str(tobj['rtds_tweet']['user_id'])
		# print id_
		# id_ = 1107232339
		n = graph_db.get_indexed_node("users", "uid", str(id_))
		
		# If that user present in main database
		if(n):
			c2+=1
			friends = graph_db.get_related_nodes(n)
			print friends
			profile =  graph_db.get_properties(n)[0]
			profile['day'] = 1
			# print profile
			graph_db_topic.get_or_create_indexed_node("users", "uid", id_, profile)
			
			# m = graph_db_topic.get_indexed_node("users", "uid", str(id_))
			# print graph_db_topic.get_properties(m)

		# break
		line = f.readline()

	print "tweets :", c1," day 1 nodes :", c2
	f.close()

def insert_day_n(loc, day, log_loc):
	
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	graph_db_topic = neo4j.GraphDatabaseService("http://localhost:7475/db/data/")
	
	c1 =0;c2 =0
	
	f = open(loc,"r")
	line = f.readline()
	window = 0

	while(line):
		
		# tobj = json.loads(line)
		# id_ = str(tobj['rtds_tweet']['user_id'])
		# id_ = 1107232339
		tobj = line.split("\t")
		id_ = tobj[0]
		ts = int(tobj[1])
		
		# intializing the window with the time_stamp of first tweet
		
		if(c1 == 0):
			window = ts
		
		n = graph_db.get_indexed_node("users", "uid", str(id_))
		c1 +=1
		
		# If that user present in main database
		if(n):
			c2+=1
			profile =  graph_db.get_properties(n)[0]
			friends = n.get_related_nodes(neo4j.Direction.OUTGOING,"follows")
			
			profile['day'] = day
			profile['ts'] = ts
			# Inserting the author if not already in topical Graph G(t)
			author = graph_db_topic.get_or_create_indexed_node("users", "uid", id_, profile)
			
			for friend in friends:
				fid = friend["uid"]
				fn = graph_db_topic.get_indexed_node("users", "uid", str(fid))
				# If my friend already present in G(t-1)
				if(fn):
					graph_db_topic.create( (author, "follows", fn))
		
		# update the window every 30 min
		# get the connected components sizes.
		if(ts > window + 30*60):
			window = ts
			l1, l2, mid, avg, l = connected_comp.main(ts)
			dump_log(log_loc,[c1, c2, l1, l2, mid, avg, l, datetime.now()])

		line = f.readline()



	f.close()



insert_day_n("/home/pranayag/neo/cluster/sorted_tweets/0.txt", 1, "/home/pranayag/neo/cluster/log0.txt")
#insert_day_n("/home/pranayag/neo/cluster/3.txt", 2, "/home/pranayag/neo/cluster/log.txt")
