from bs4 import BeautifulSoup
# import urllib2
import os

def get_1():
	html_doc = """
	<html><head><title>The Dormouse's story</title></head>

	<p class="title"><b>The Dormouse's story</b></p>

	<p class="story">Once upon a time there were three little sisters; and their names were
	<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
	<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>

	<p class="story">...</p>
	"""
	html_doc = open('people.html',"r").read()
	soup = BeautifulSoup(html_doc)

	# print(soup.prettify())
	print (soup.get_text())
	# print (soup.p)
	# print (soup.div)
	# print (soup.find_all('a',{"class" : 'various fancybox.ajax'})[13])

	# f = open('people.html',"r")
	# lines = f.readlines()
	# soup = BeautifulSoup(lines)
	# print(soup.prettify())
	# f.close()


	# for line in lines:
	# 	if(line.find("@")>0):
	# 		print line


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