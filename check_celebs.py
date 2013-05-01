from py2neo import neo4j
import json
from pprint import pprint


graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

f = open('celebs.txt',"r")
entry = json.loads(f.readline())

celebs =  json.loads(entry['users'])
for celeb in celebs:
	id_ = str(celeb["id"])

	n = graph_db.get_indexed_node("users", "uid", id_)
	if(n):
		print graph_db.get_properties(n)