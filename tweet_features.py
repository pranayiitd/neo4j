import json
from pprint import pprint
from datetime import datetime
import os
import sys
import json

def dump_log(loc, arr):
	f = open(loc,"a")
	s =""	
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	f.write(s)
	f.close()


def cal_retweet(tweet):
	pass

def cal_mention(tweet):
	pass

def cal_url(tweet):
	pass

def cal_hashtag(tweet):
	pass

def cal_stats(rt, mentions, url, hashtag, map_data, count_data):
	pass


def main():
	loc = ""
	dst = ""
	
	

	f_list = os.list(loc)
	for fl in f_list:
		
		f = open(loc+fl,"r")
		fo = open(dst+fl,"w")

		# STATICS OF ONE TWEET CLUSTER
		rt_map = {}
		url_map = {}
		mentions_map = {}
		htags_map = {}

		map_data = [rt_map, url_map, mentions_map, htags_map]
		
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
			if(c1 == 1):
				window = ts
			
			line = line.replace("\n","")
			row  = line.split("\t")
			tweet = row[2]
			ts = row[1]
			

			rt = cal_retweet(tweet)
			mentions = cal_mention(tweet)
			url = cal_url(tweet)
			hashtag = cal_hashtag(tweet)
			
			cal_stats(rt, mentions, url, hashtag, map_data, count_data)

			# For evey 30 min window write the stats
			
			if(ts > window + 30*60):
				window = ts
				# dump_log(loc, [c1, datetime.now()])
				dump_log(dst+fl,[c1, rt_count, mentions_count, urls_count, htags_count, datetime.now()])

			line = f.readline()

		f.close()

		f = open(dst+fl+"_stats","w")
		for dic in map_data:
			f.write(json.dumps(dic)+"\n")
		f.close()