# Get all tweet object containg the topic keywords in the text
# A naitve to get all the tweets related to particular topic.



wimport json
from pprint import pprint
from datetime import datetime
import os



def has_word(text):
	keys = ['Camarillo', 'fire', 'a']
	tf = False
	# print text
	for k in keys:
		if(text.lower().find(k.lower())>=0):
			tf = True
			# print k
			break
	return tf


dest ="/home/pranayag/neo/cluster/camarillo-fire.txt"
fw = open(dest,"w")

loc = "/home/y/var/timesense/data/twitter_rawTweets/en-US/syc/2013-05-02/"
files = os.listdir(loc)
for fil in files:
	f = open(loc+fil,"r")
	line = f.readline()
	while line:
		tobj = json.loads(line)
		if(has_word(tobj['rtds_tweet']['text'])):
			fw.write(line)
		line = f.readline()
	f.close()
