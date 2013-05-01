from bs4 import BeautifulSoup


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


def get_2():
	html_doc = open('p2.html',"r").read()
	soup = BeautifulSoup(html_doc)
	l = soup.find_all('td',{"class" : 'statcol_name'})
	for elem in l :
		s = elem.contents[1].contents[0]
		print(s[1+s.find('('):s.find(")")])
		# break
		# print (elem.contents[1].contents[0])

	# print(l)
	# print(l.string)
	# print(l.contents[1].contents)

get_2()