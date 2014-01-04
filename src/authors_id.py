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

loc = "/home/pranayag/neo/cluster/sorted_tweets/1.txt"	
# log = "/home/pranayag/neo/logs/angelina_graph_log.txt"

authors_set = set()

f = open(loc, "r")
line = f.readline()

while line:
	line = line.replace("\n", "")
	row = line.split("\t")
	author_id = int(row[0])
	authors_set.add(author_id)
	line = f.readline()

f.close()

f = open("/home/pranayag/neo/cluster/authors_info/1.txt","w")

arr = list(authors_set)	

for i in range(len(arr)):
	end = i+100
	if(end > len(arr)):
		end = len(arr)
	f.write(json.dumps(arr[i:end])+"\n")

f.close()	