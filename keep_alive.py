import os
import time


a = os.popen("ps -A|grep python")
s = a.read()
process_arr = s.split("\n")

target = "/home/pranayag/neo/src/resolve_all.py"
# target = "test.py"

is_alive = False


for process in process_arr:
	arr = process.split()
	if(arr!=[]):
		if(arr[len(arr)-1] == target):
			is_alive = True
			break

if(is_alive == False):

	os.system("python "+target+" &")
	# p = subprocess.Popen([sys.executable, 'test.py'], 
                                    # stdout=subprocess.PIPE, 
                                    # stderr=subprocess.STDOUT)
	# print "running...."
# else:
# 	print "already running! :)"


# a = os.popen("ps -A|grep python")
# s = a.read()
# process_arr = s.split("\n")
# print process_arr
