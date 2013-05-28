# -*- coding: UTF-8 -*-
__author__ = 'song'
import kmeans

def test():
    a = 0
    def t():
        print a
        a = 1
    t()
    print a

test()