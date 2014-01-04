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

def sort_sample():
	src_loc = "sample.txt"
	dst_loc = "sorted.txt"

	arr = []

	f = open(src_loc, "r")
	line = f.readline()

	while line:
		tobj = json.loads(line)
		uid = str(tobj['rtds_tweet']['user_id'])
		ts  = str(tobj['rtds_tweet']['created_at'])
		arr.append((uid, ts))
		
		line = f.readline()

	# print arr[0]
	f.close()
	arr.sort(key=lambda tup: tup[1])

	# print arr

	f = open(dst_loc, "w")

	for a in arr:
		f.write(a[0]+"\t"+a[1]+"\n")

	f.close()


# SORTS ALL THE TWEET FILE IN SRC BY TIME_STAMP AND DUMP AT DST
def sort_folder(src, dst):
	f_list = os.listdir(src)
	for fil in f_list:
		tweet_arr =[]
		
		f = open(src+fil,"r")
		
		line = f.readline()
		while line:
			line = line.replace("\n","")
			tweet_row = line.split("\t")
			uid = int(tweet_row[0])
			ts = int(tweet_row[1])
			text =tweet_row[2]
			tweet_arr.append((uid, ts, text))
			line = f.readline()

		f.close()
		tweet_arr.sort(key = lambda tup : tup[1])

		f = open(dst+fil,"w")
		for a in tweet_arr:
			f.write(make_row([a[0], a[1], a[2]]))
		f.close()


src = "/home/pranayag/neo/cluster/raw/"
dst = "/home/pranayag/neo/cluster/sorted_tweets/"

sort_folder(src, dst)





