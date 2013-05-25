import os
import time
import test

a = os.popen("ps -A|grep python")
s = a.read()
process_arr = s.split("\n")
# print process_arr
target = "test.py"
is_alive = False


while(True):

	for process in process_arr:
		 arr = process.split()
		 if(arr!=[]):
		 	if(arr[len(arr)-1] == target):
		 		is_alive = True
		 		break

	if(is_alive):
		print target,"is Running..."
	else:
		print target,"is NOT Running.Restarting Now."
		# os.system("python test.py")
		test.main()
		print "returned from callee"
		is_alive = False
	
	print "sleeping 10 secs..."
	time.sleep(10)	