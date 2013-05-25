import time
from datetime import datetime

def main():
	# time.sleep(50)
	f = open("dump.txt","a")
	for i in range(5):
		print i
		time.sleep(1)
		f.write(str(datetime.now())+"\n")

	# return "the return value"
	f.close()

main()
