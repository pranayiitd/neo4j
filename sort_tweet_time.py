import json
from pprint import pprint
from datetime import datetime


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

