import json
from pprint import pprint
from datetime import datetime
import os
import sys
import json
import re

def print_arr(count, arr):
	s = 0
	for i in range(count):
		v = int(arr[len(arr) - 1 - i][1])
		s += v
	return s

def urls_analyze():
	loc = "/Users/pranayag/mtp/visualize/analysis_stats/0.txt_urls"
	urls_map = {}
	
	f = open(loc, "r")
	line = f.readline()
	while line:
		line = line.replace("\n", "")
		row = line.split("\t")
		count = int(row[0])
		url = row[2]
		if(urls_map.has_key(url)):
			urls_map[url] += count
		else:
			urls_map[url] = count

		line = f.readline()

	urls_arr = urls_map.items()
	urls_arr.sort(key = lambda tup : tup[1])
	print "urls\n",sum(urls_map.values()),len(urls_map)
	print print_arr(100, urls_arr)
	# print urls_arr[len(urls_arr)-50: len(urls_arr)]
	# print len(urls_arr)




loc = "/Users/pranayag/mtp/visualize/analysis_stats/0.txt_stats"

f = open(loc, "r")
rt_map = json.loads(f.readline())
mentions_map = json.loads(f.readline())
urls_map = json.loads(f.readline())
htags_map = json.loads(f.readline())

mentions_arr = mentions_map.items()
mentions_arr.sort(key = lambda tup:tup[1])
print "mentions\n",sum(mentions_map.values()),len(mentions_map)
print print_arr(100, mentions_arr)
# print mentions_arr[len(mentions_arr)-100 :len(mentions_arr)]

# urls_arr = urls_map.items()
# urls_arr.sort(key = lambda tup : tup[1])
# print "urls\n",sum(urls_map.values())
# print print_arr(100, urls_arr)
# print urls_arr[len(urls_arr)-50: len(urls_arr)]
# print len(urls_arr)

urls_analyze()
htags_arr = htags_map.items()
htags_arr.sort(key = lambda tup: tup[1])
print "htags\n",sum(htags_map.values()),len(htags_map)
print print_arr(100, htags_arr)

# print htags_arr[len(htags_arr)-20 : len(htags_arr)]




f.close()

