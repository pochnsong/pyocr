#coding=utf8
__author__ = 'song'
import math


def match_distance_by_block(feature1, feature2):
    """
    按特征的分块特征进行匹配
    feature1, feature2 为分块特征
    """
    res = []
    for block in range(len(feature1)):
        I = 0
        for i in range(len(feature1[block])):
            I += abs(feature1[block][i]-feature2[block][i])
        res.append(I)

    return res


def similarity(vector1, vector2):

    tmp0 = 0
    tmp1 = 0
    tmp2 = 0
    for i in range(len(vector1)):
        tmp0 += vector1[i]*vector2[i]
        tmp1 += pow(vector1[i], 2)
        tmp2 += pow(vector2[i], 2)

    res = float(tmp0)/(math.sqrt(tmp1)*math.sqrt(tmp2))
    return res


def match_similarity_by_block(feature1, feature2):
    """
    按特征的分块特征进行匹配
    feature1, feature2 为分块特征
    """
    res = []
    for block in range(len(feature1)):
        I = similarity(feature1[block], feature2[block])
        res.append(I)

    return res
