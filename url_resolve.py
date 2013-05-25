import json
from pprint import pprint
from datetime import datetime
import os
import sys
import json
import re
import urllib2

def unshorten(short_url):
	api = "http://api.unshort.me/?r="+short_url+"&t=json"
	resp = urllib2.urlopen(api).read()
	obj = json.loads(resp)
	return obj['resolvedURL']


# loc = "/Users/pranayag/mtp/visualize/analysis_stats/0.txt_stats"
# dst = "/Users/pranayag/mtp/visualize/analysis_stats/0.txt_urls"

loc = "/home/pranayag/neo/cluster/stats/0.txt_stats"
dst = "/home/pranayag/neo/cluster/stats/0.txt_urls"

f = open(loc, "r")
fw = open(dst, "w")

rt_map = json.loads(f.readline())
mentions_map = json.loads(f.readline())
urls_map = json.loads(f.readline())
htags_map = json.loads(f.readline())

urls_arr = urls_map.items()
urls_arr.sort(key = lambda tup : tup[1])

for tup in urls_arr:
	short_url = tup[0]
	count = tup[1]
	long_url = short_url
	status = "1"
		
	if(len(short_url) > 12 ) :
		# long_url = unshorten(short_url)
		try:
			long_url = unshorten(short_url)
		except:
			long_url = short_url
			status = "-1"
		fw.write(str(count)+"\t"+short_url+"\t"+long_url+"\t"+status+"\n")
	# break

f.close()
fw.close()