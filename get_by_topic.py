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

		for key in tup:
			# key = tup[k]
			if(text.lower().find(key.lower()) < 0):
				temp = False
				break
		tf = temp
		if(tf):
			break
	print arr,tf
	return tf


def cluster_tweet(text, topic_map, clusters):
	# text = tobj[['rtds_tweet']['text']]
	# uid  = tobj
	# ts   = 
	# Look for all the clusters.
	uid = 1
	ts = 1
	for key in topic_map.keys():
		print key
		if(has_word(text, topic_map[key])):
			clusters[key].write(make_row([uid, ts, text]))
			# print topic_map[key]



def main():

	topic_map = {
				   0 : [["irs", "scandal"]],
				   1 : [["angelina", "jolie"], ["mastectomy"]],
				   2 : [["cannes"], ["film", "festival"]],
				   3 : [["scandal", "obama"]],
				   4 : [["google", "io"]],
				   5 : [["gatsby"]]
				}

	clusters =[]

	# LOCATION FOR CLUSTERS DUMP
	dst ="../y_trends/"

	for i in range(len(topic_map)):
		f = open(dst+str(i)+".txt","a")
		clusters.append(f)

	tobj = "Je dis pas des renvois de cours heiin mais taay 3jours doyoumeeuu"
	cluster_tweet(tobj, topic_map, clusters)
	return
	

	# SEARCHING THE FILTERED TWEETS TO BE CLUSTERED.
	loc = "/home/y/var/timesense/data/twitter_rawTweets/en-US/syc/"
	folders =["2013-05-14","2013-05-15","2013-05-16"]

	for folder in folders:
		files = os.listdir(loc+folder)
		for fil in files:
			f = open(loc+fil,"r")
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
main()