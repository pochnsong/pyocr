# -*- coding: UTF-8 -*-
__author__ = 'song'
import kmeans

data =[1, 100,200,300,400,500]
k = kmeans.KMeans(2)
k.SetCenter([0,500])
k.SetData(data)

k.Run()

print k.Group[0]
print k.Group[1]