# A web crawler to get celebs from the web.

from bs4 import BeautifulSoup
# import urllib2
import os

def get_celeb_list():
	files = os.listdir('celebs/web')
	# print(files)
	fw = open('celebs/top1000.txt',"a")

	for fil in files:
		html_doc = open('celebs/web/'+fil,"r").read()
		soup = BeautifulSoup(html_doc)
		l = soup.find_all('td',{"class" : 'statcol_name'})
		for elem in l :
			s = elem.contents[1].contents[0]
			uname = s[1+s.find('('):s.find(")")]
			fw.write(uname+"\n")
		# break

	fw.close()
	

def get_from_web():
	for i in range(1,11):
		url = "http://twitaholic.com/top"+str(i)+"00/followers/"
		page = urllib2.urlopen(url).read()
		f = open('celebs/web/top'+str(i)+"00.html","w")
		f.write(page)
		f.close()

# get_2()
# get_from_web()
get_celeb_list()