import json
from pprint import pprint
from datetime import datetime
import os
import sys
import json
import re

def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()


def cal_retweet(tweet):
	tf = False
	if(tweet.find("RT ")>= 0):
		tf = True	
	return tf

def cal_mention(tweet):
	mentions = []
	arr = list(re.finditer("(?<!\w)@\w+", tweet))
	for tup in arr:
		mentions.append(tweet[tup.start(): tup.end()])
	return mentions


def cal_url(tweet):
	# print tweet
	urls = []
	arr = list(re.finditer("https?\S+", tweet))
	for tup in arr:
		urls.append(tweet[tup.start(): tup.end()])
	# print urls
	return urls

def cal_hashtag(tweet):
	# print tweet
	htags = []
	arr = list(re.finditer("(?<!\w)#\w+", tweet))
	for tup in arr:
		htags.append(tweet[tup.start(): tup.end()])
	# print htags
	return htags


def cal_stats(rt, mentions, urls, htags, map_data, count_data):
	# print rt, mentions, urls, hashtags, map_data, count_data
	
	# If the tweet is retweet
	if(rt):
		count_data[0] += 1
	
	# IF tweet contains mentions
	if(len(mentions) > 0):
		mentions_map = map_data[1]
		count_data[1] += len(mentions)
		for mention in mentions:
			if(mentions_map.has_key(mention)):
				mentions_map[mention] += 1
			else:
				mentions_map[mention] = 1

	# If the tweet contains URLs
	if(len(urls) > 0):
		urls_map = map_data[2]
		count_data[2] += len(urls)
		for url in urls:
			if(urls_map.has_key(url)):
				urls_map[url] += 1
			else:
				urls_map[url] = 1

	if(len(htags) > 0):
		htags_map = map_data[3]
		count_data[3] += len(htags)
		for tag in htags:
			if(htags_map.has_key(tag)):
				htags_map[tag] += 1
			else:
				htags_map[tag] = 1

 
def main():
	loc = "/home/pranayag/neo/cluster/sorted_tweets/"
	dst = "/home/pranayag/neo/cluster/stats/"
	
	f_list = os.listdir(loc)
	
	for fl in f_list:
		
		f = open(loc+fl,"r")
		fo = open(dst+fl,"w")

		# STATICS OF ONE TWEET CLUSTER
		rt_map = {}
		urls_map = {}
		mentions_map = {}
		htags_map = {}

		map_data = [rt_map, urls_map, mentions_map, htags_map]
		
		rt_count = 0
		mentions_count = 0
		urls_count = 0
		htags_count = 0
		count_data = [rt_count, mentions_count, urls_count, htags_count]
		
		window = 0 ; ts = 0
		c1 = 0
		line = f.readline()
		
		while line:
			c1+=1
			
			
			line = line.replace("\n","")
			row  = line.split("\t")
			tweet = row[2]
			ts = row[1]

			# tobj = json.loads(line)
			# tweet = tobj['rtds_tweet']['text'].encode("ascii","ignore")
			# ts = tobj['rtds_tweet']['created_at']


			if(c1 == 1):
				window = ts
			rt = cal_retweet(tweet)
			mentions = cal_mention(tweet)
			urls = cal_url(tweet)
			htags = cal_hashtag(tweet)
			
			cal_stats(rt, mentions, urls, htags, map_data, count_data)

			# For evey 30 min window write the stats
			if(ts > window + 30*60):
				window = ts
				dump_log(dst+fl,[c1]+ count_data +[datetime.now()])


			# break
			line = f.readline()

		# DUMP DATA FROM THE LAST WINDOW IF NOT DONE
		dump_log(dst+fl,[c1]+ count_data +[datetime.now()])
		f.close()

		f = open(dst+fl+"_stats","w")
		for dic in map_data:
			f.write(json.dumps(dic)+"\n")
		f.close()

main()		