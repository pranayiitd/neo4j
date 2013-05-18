# Get all tweet object containg the topic keywords in the text
# A naitve to get all the tweets related to particular topic.

import json
from pprint import pprint
from datetime import datetime
import os

def make_row(arr):	
	s =""
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	return s


# Check if the text contains any tuple(but all keys in a tuple) of the array
def has_word(text, arr):
	tf = False
	for tup in arr:
		temp = True
		for k in tup:
			if(text.lower().find(k.lower()) < 0):
				temp = False
				break
		tf = temp
		if(tf):
			break
	return tf


def cluster_tweet(tobj, topic_map, clusters):
	text = tobj['rtds_tweet']['text'].encode("ascii","ignore")
	uid = str(tobj['rtds_tweet']['user_id'])
	ts  = str(tobj['rtds_tweet']['created_at'])
	# Look for all the clusters.
	for key in topic_map.keys():
		if(has_word(text, topic_map[key])):
			f = clusters[key]
			#print f
			f.write(make_row([uid, ts, text]))




topic_map = {
				   0 : [["irs", "scandal"]],
				   1 : [["angelina", "jolie"], ["mastectomy"]],
				   2 : [["cannes"], ["film", "festival"]],
				   3 : [["scandal", "obama"]],
				   4 : [["google", "io"],["i/o"]],
				   5 : [["gatsby"]]
			}

clusters =[]

# LOCATION FOR CLUSTERS DUMP
dst ="/home/pranayag/neo/cluster/"

for i in range(len(topic_map)):
	f = open(dst+str(i)+".txt","a")
	clusters.append(f)



# SEARCHING THE FILTERED TWEETS TO BE CLUSTERED.
loc = "/home/y/var/timesense/data/twitter_rawTweets/en-US/syc/"
folders =["2013-05-14","2013-05-15","2013-05-16"]
#folders =["2013-05-16"]
for folder in folders:
	files = os.listdir(loc+folder)
	for fil in files:
		f = open(loc+folder+"/"+fil,"r")
		line = f.readline()
		while line:
			tobj = json.loads(line)
			# Decide the cluster and dump at the right place.
			cluster_tweet(tobj, topic_map, clusters)
			line = f.readline()
		f.close()

# Closing the file descp
for fo in clusters:
	fo.close()
