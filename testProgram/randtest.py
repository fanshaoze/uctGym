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


import numpy as np

count = 10 ** 5


def func1():
    random.random()


def func2():
    int(random.random() * 4)


def func3():
    random.randint(0, 4)


def func4():
    int(os.urandom(4).hex(), 16)


def func5():
    hashlib.md5("md5 test".encode("utf-8"))


def func6():
    np.random.rand()


def func7():
    np.random.random_integers(0, 0xffff)


def func8():
    np.random.randint(4)


def func9():
    global b, count
    b = np.random.randint(5, size=1)


def func10():
    a = [i for i in range(0, count)]
    random.shuffle(a)


def func11():
    l = []
    for i in range(0, count):
        l.append(random.randint(0, 0xffff))


def func12():
    random.getrandbits(2)


def func13():
    random.getrandbits(32)


print('random.random()                        ', timeit.timeit(func1, number=count))
print('np.random.rand()                       ', timeit.timeit(func6, number=count))
print("*" * 20)
print('int(random.random()*0xffff)            ', timeit.timeit(func2, number=count))
print('random.randint(0, 0xffff)              ', timeit.timeit(func3, number=count))
print('int(os.urandom(4).hex(),16)            ', timeit.timeit(func4, number=count))
print('hashlib.md5("md5 test".encode("utf-8"))', timeit.timeit(func5, number=count))
print('np.random.randint(0xffff)              ', timeit.timeit(func8, number=count))
print('Crypto.Random.random.getrandbits(32)   ', timeit.timeit(func12, number=count))
print('random.getrandbits(32)                 ', timeit.timeit(func13, number=count))
print("*" * 20)
print('l.append(random.randint(0, 0xffff))    ', timeit.timeit(func11, number=1))
print('np.random.randint(0xffff,size=count)   ', timeit.timeit(func9, number=1))
print('random.shuffle(a)                      ', timeit.timeit(func10, number=1))
