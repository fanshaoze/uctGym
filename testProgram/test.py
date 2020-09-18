import _thread
import threading
import time
import sys
import math
import random
import datetime
from multiprocessing import Process
import cProfile
from multiprocessing import Pool

def multiprocessing_test():
	print ("Start : %s" % time.ctime())
	time.sleep(10)
	print ("End : %s" % time.ctime())
	print("ok!")

# def main():
# 	a = "123123123"
# 	b = ""
# 	for i in range(0,len(a),3):
# 		b+=a[i:i+3]+"\n"
# 	print(b)
#
# 	# threadNum = 4
# 	# threads = []
# 	# for i in range(0, threadNum):
# 	# 	t = Process(target=multiprocessing_test, args=())
# 	# 	threads.append(t)
# 	# 	t.start()
#
# if __name__ == "__main__":
# 	main()
