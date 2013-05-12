# For a given topic it will make anothe neo4j instance for topical graph of the
# given topic. 
# Then making it evolving graph.

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

def insert_day_n(loc, day):
	
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
	graph_db_topic = neo4j.GraphDatabaseService("http://localhost:7475/db/data/")
	
	c1 =0;c2 =0
	
	f = open(loc,"r")
	line = f.readline()
	while(line):
		c1 +=1
		tobj = json.loads(line)
		id_ = str(tobj['rtds_tweet']['user_id'])
		# id_ = 1107232339
		n = graph_db.get_indexed_node("users", "uid", str(id_))
		
		# If that user present in main database
		if(n):
			c2+=1
			profile =  graph_db.get_properties(n)[0]
			friends = n.get_related_nodes(neo4j.Direction.OUTGOING,"follows")
			
			profile['day'] = day
			# Inserting the author if not already in topical Graph G(t)
			author = graph_db_topic.get_or_create_indexed_node("users", "uid", id_, profile)
			
			for friend in friends:
				fid = friends[uid]
				fn = graph_db_topic.get_indexed_node("users", "uid", str(fid))
				# If my friend already present in G(t-1)
				if(fn):
					graph_db_topic.create( (author, "follows", fn))


		line = f.readline()



	f.close()
	print "tweets :", c1," day ", n ,"nodes :", c2



insert_day_1("/home/pranayag/neo/cluster/camarillo-fire-2.txt")
insert_day_n("/home/pranayag/neo/cluster/camarillo-fire-3.txt", 2)
