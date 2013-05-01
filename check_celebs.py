from py2neo import neo4j
import json
from pprint import pprint


graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

f = open('celebs/top_profile.txt',"r")
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