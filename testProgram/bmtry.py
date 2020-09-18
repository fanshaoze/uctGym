import cProfile
from abc import ABCMeta, abstractmethod
import copy
import datetime
import random
import numpy as np

class Test():
    def __init__(self, name):
        self.name = name
        print('这是构造函数')

    def say_hi(self):
        print('hell, %s' % self.name)

    def __del__(self):
        print('这是析构函数')



class Base(object):
    tests = []
    __metaclass__=ABCMeta #必须先声明
    def __init__(self,testB):
        self.testB = testB
        pass
    #@abstractmethod #虚函数
    def get(self):
        print('base get')
        pass
    def testprint(self):
        print ("123")

class Derivel(Base):
    def get(self):
        print("Derivel get")

class Derivel2(Base):
    def get(self):
        print("Derivel2 get")
    def testprint(self):
        print("not know")
    def testprint(self,canbe):
        print("know it canbe",canbe)


def getinfo(name, age, hoppy=-1):
    if hoppy>0:
        print("name:", name.title(), "age:", age, "hoppy:", hoppy)
    else:
        print("name:", name.title(), "age:", age)

getinfo('mike', 25)
getinfo('mike', 25, 3)

C = Test("bigberg")
D = Base(C)
print("isinstance:",not isinstance(D,Base))
A = Derivel(C)
A.testB.say_hi()

A.get()
A.tests.append(C)
A.tests.append(C)
A.tests[0].say_hi()
#B.get()
A.testprint()

print(type(A))
print(type(D))
if type(D) == Base:
    print('yes')
#print(type(Base))


print("-----------------------------------------")
B = Derivel2(C)
E = copy.deepcopy(B)
E.testprint(123)
print("E:",E," B:",B)
B.testprint(123)
x = A.testB
print("a.1",A.testB.name)
x.name = "1234"
print("a.2",A.testB.name)
print("********************************")
del C
def trypart(a):
    a = 3
    return a

for num in range(10,20):  # 迭代 10 到 20 之间的数字
   for i in range(2,num): # 根据因子迭代
      if num%i == 0:      # 确定第一个因子
         j=num/i          # 计算第二个因子
         print ('%d 等于 %d * %d' % (num,i,j))
         break            # 跳出当前循环
   else:                  # 循环的 else 部分
      print (num, '是一个质数')
for i in range (0,0):
    print("at least once")
x1 = 0
x1 = trypart(x1)
print(x1)

dict1= {0:4,1:5,2:6}
dict2 = dict1.copy()
print(dict2)
dict2[0]= 7
print(dict2)
print(dict1)
dict2[3] = dict2[0]
del dict2[0]
print("00000000000000000000000000000000000")
print(dict2)
print(dict1)
D1 = {'user': 'runoob', 'num': [1, 2, 3]} # 原始数据
D2 = D1  # 直接引用：D2和D1整体指向同一对象。
D3 = D1.copy()  # 浅拷贝：D3和D1的父对象是一个独立的对象，但是他们的子对象还是指向同一对象。
D4 = copy.deepcopy(D1)  # 深拷贝：D4和D1的整体是一个独立的对象。

D1['user'] = 'root' # 修改父对象D1
D1['num'].remove(1) # 修改父对象D1中的[1, 2, 3]列表子对象

print('原始数据:',{'user': 'runoob', 'num': [1, 2, 3]}) # 原始数据
print('改后数据:',D1) # 父子都修改过的
print('直接引用:',D2) # 父子都变(直接引用)
print('浅拷贝:',D3) # 父不变，子变(浅拷贝)
print('深拷贝:',D4) # 父子都不变(深拷贝)

E1 = [1,2,3]
E2 = [4,5,6]
E3 = dict(zip(E1,E2))
print(E3)
print(4 in E3.values())
fo = open("initdiff-test.txt", "w")
for max_depth in range(0,2):
    for num_Runs in range(0,2):
        avgsteps = 100
        fo.write(str(max_depth)+","+str(num_Runs)+","+str(avgsteps)+"\n")
fo.close()

postion = [(1,2,3),(4,5,6)]
print("postion[0][0]",postion[0][0])



#time of rand
starttime = datetime.datetime.now()
for i in range(0,100000000):
    random.randint(0,4)
endtime = datetime.datetime.now()
print("execute time: ",(endtime - starttime).microseconds)

starttime = datetime.datetime.now()
for i in range(0,100000000):
    int(random.random()*4)
#np.random.randint(low=0,high = 5,size=10000000)
endtime = datetime.datetime.now()
print("execute time: ",(endtime - starttime).microseconds)

starttime = datetime.datetime.now()
for i in range(0,100000000):
    random.getrandbits(2)
#np.random.randint(low=0,high = 5,size=10000000)
endtime = datetime.datetime.now()
print("execute time: ",(endtime - starttime).microseconds)

