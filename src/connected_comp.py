from py2neo import neo4j, cypher
import json
from pprint import pprint
from datetime import datetime

# Finding out the largest, second largest connected component in the graph

graph_component = {}
gcount =0

def handle_row(row):
	node = row[0]
	global gcount
	gcount+=1
	global time_stamp

	# if(gcount %1000==0):
	# 	print gcount
	
	rf = False
	if(node['time_stamp'] == None):
		rf = True
	else:
		if(node['time_stamp'] != time_stamp):
			rf = True
	

	if(rf==True):
		global graph_component
		cid = len(graph_component)
		node['visited'] = cid
			
		bfs(node, cid, graph_component, time_stamp)
		#print graph_component[cid],node['uid']		
	else:
		return

# Does a BFS
def bfs(node, cid, graph_component, time_stamp):
	
	tf = False

	if(node['time_stamp'] == None):
		tf = True
	else:
		if(node['time_stamp'] != time_stamp):
			tf = True

	if(tf != True):
		return
	
	if(graph_component.has_key(cid) == False):
		graph_component[cid] = 1
	else:
		graph_component[cid] += 1
	
	
	node['time_stamp'] = time_stamp

	rels = node.get_related_nodes(neo4j.Direction.BOTH, "follows")
	
	for rel in rels:
		bfs(rel, cid, graph_component, time_stamp)
		

time_stamp = 2

# Returns the largest and second largest connected component size
# at time time ts.
def main(ts):
	global time_stamp
	time_stamp = ts
	global graph_component
	graph_component ={}
	# print time_stamp	
	# print " Start the BFS..."
	graph_db = neo4j.GraphDatabaseService("http://localhost:7475/db/data/")
	# print " connected to DB."
	cypher.execute(graph_db, "START z=node(*) RETURN z", row_handler=handle_row)
	return get_comp_sizes(graph_component.values())


# Returns highest, and second higest value in the array.
def get_comp_sizes(arr):
	#print arr
	arr.sort()
	l = len(arr)
	one = arr[l-1]
	two = arr[l-2]
	median = arr[l/2]
	avg = sum(arr)/l
	
	return[one, two, median, avg, l ]

#print main(3)
