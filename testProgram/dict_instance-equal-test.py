# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:57:55 2019

@author: sidanzhang
"""

import timeit
import random
import time
import datetime
import json
import hashlib
import os


class test:

	def __init__(self,invar,var2,var3,var4):
		self.invar=invar
		self.var2=var2
		self.var3=var3
		self.var4=var4

print(test.__dict__)

t1=test(1,2,3,4)
t2=test(1,2,3,1)
starttime = datetime.datetime.now()
for i in range(0,1000000):
	print(t1.invar == t2.invar and t1.var2 ==t2.var2 and t1.var3 ==t2.var3 and t1.var4 ==t2.var4)
endtime = datetime.datetime.now()
time1 = (endtime - starttime).microseconds
print("-------------------------------------------------------------------------")
starttime = datetime.datetime.now()
for i in range(0,1000000):
	print(t1.__dict__==t2.__dict__)
endtime = datetime.datetime.now()
time2 = (endtime - starttime).microseconds
print (time1)
print (time2)

