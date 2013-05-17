import urllib2
import json
from pprint import pprint

def make_row(arr):	
	s =""
	for elem in arr:
		s = s+str(elem)+"\t"
	s = s+"\n"
	return s

# GET "COUNT" NUMBER OF TOP TRENDING TOPICS AND DUMP IN "DST"
def y_buzzing(count, dst):
	
	fout = open(dst, "w")
	api_server = "http://api01.timesense.sp2.yahoo.com:4080/timesense/v3/en-US-TWITTER/topbuzzing?count="
	api_query = api_server+str(count)
	f = urllib2.urlopen(api_query)
	response = f.read()
	resp_json = json.loads(response)

	for t in resp_json['topics']: 
		topic 	 = t['title']
		topic_id = t['id']
		score    = t['score']
		fout.write(make_row([topic_id, topic, score]))

# GET RELATED TWEETS TO TOPIC IN "TOPIC_LIST" AND DUMP
# def trend_tweets(topic_list, loc):
	







y_buzzing(1000, "../y_trends/buzzing.txt")