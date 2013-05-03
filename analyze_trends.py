import json
from pprint import pprint
from datetime import datetime
import os

def topics_list():
	loc = "/home/pranayag/india/topics/"
	files = os.listdir(loc)
	topics ={}
	# print files
	for f in files:
		fo = open(loc+f,"r")
		line = fo.readline()
		trends = json.loads(json.loads(line)['trends'])[0]['trends']
		for t in trends:
			# print t['name']
			if((topics.has_key(t['name'])) == True):
				topics[t['name']]+=1
			else:
				topics[t['name']] = 1
		# pprint(trends[0])
		# break

	data = topics.items()
	data.sort(key=lambda tup: tup[1])
	return data

def cluster_dump(data, t):
	text = t['text'].lower()
	# print text
	for d in data:
		if(text.find(d[0].lower()) >0 ):
			# print d
			d[2].write(json.dumps(t)+"\n")



def cluster_tweet():
	data = topics_list()
	l1 ="/home/pranayag/india/cluster/"
	
	for i in range(len(data)):
		f = open(l1+data[i][0],"w")
		data[i] =  data[i]+(f,)

	loc = "/home/pranayag/india/tweets/"
	files = os.listdir(loc)
	for fil  in files:
		f = open(loc+fil,"r")
		line = f.readline()
		tweets = json.loads(json.loads(line)['tweets'])['statuses']
		for t in tweets:
			cluster_dump(data, t)
			# print t['text'].lower().find('Earth'.lower())

cluster_tweet()	