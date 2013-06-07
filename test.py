# -*- coding: UTF-8 -*-
__author__ = 'song'
import ocr_feature_extraction
import ocr_match

import Image
import glob
import jft

get_feature = ocr_feature_extraction.get_outside_feature3

print "load ... "
database = {}
#print glob.glob("tools/image1/*.png")
for name in glob.glob("tools/image1/*.png"):
    word = name.split("/")[2].split(".")[0]
    feature = get_feature(Image.open(name))
    database[word] = feature

print "ok"

print "match"
for name in glob.glob("test/*.png"):
    me = name.split("/")[1].split(".")[0]

    feature1 = get_feature(Image.open(name))
    res = {}
    for word in database.keys():
        match = ocr_match.match_similarity_by_block(feature1, database[word])
        match = sum(match)
        if res.has_key(match):
            res[match].append(word)
        else:
            res[match] = [word]

    keys = sorted(res, reverse=True)
    sss = ""
    print name, me,
    for i in range(100):
        sss += " "+res[keys[i]][0]
        if me == res[keys[i]][0]:
            print "Find",
    print sss


'''
#w1 = Image.open("tools/image1/避.png")
zi = "觀"
w2 = Image.open("test/"+zi+".png")


#f1 = ocr_feature_extraction.get_outside_feature(w1)
f2 = get_feature(w2)

res = {}
res_sum = {}
for word in database.keys():
    tmp = ocr_match.match_similarity_by_block(database[word], f2)
    res_sum[word] = sum(tmp)
    res[word] = tmp

i = 0
for key, value in sorted(res_sum.items(), lambda x, y: cmp(x[1], y[1])):
    i += 1
    print zi, key, value, res[key], i
    if zi == key:
        sss = raw_input()

'''