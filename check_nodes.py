from py2neo import neo4j
import json
from pprint import pprint


def celebs():
	
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

	f = open('/home/pranayag/neo/src/celebs/top_profile.txt',"r")
	line = f.readline()
	count =0

	while line:
		entry = json.loads(line)
		celebs =  json.loads(entry['users'])
		
		# Checking if celeb in database.
		for celeb in celebs:
			id_ = str(celeb["id"])
			n = graph_db.get_indexed_node("users", "uid", id_)
			if(n):
				count+=1
				print graph_db.get_properties(n)

		line = f.readline()

	f.close()

	print count			

def trending_nodes():
	graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

	f = open('/home/pranayag/neo/cluster/camarillo-fire-3.txt',"r")
	line = f.readline()
	count =0

	while line:
		tobj = json.loads(line)
		id_ = str(tobj['rtds_tweet']['user_id'])
		n = graph_db.get_indexed_node("users", "uid", id_)
		if(n):
			count+=1
			#print graph_db.get_properties(n)
		
		line = f.readline()

	f.close()

	print count


trending_nodes()	
