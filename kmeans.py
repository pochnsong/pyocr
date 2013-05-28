#coding=utf8

__author__ = 'song'
import math

class KMeans:
    def __init__(self, K):
        self.K = K
        self.Group = {}
        for k in range(K):
            self.Group[k] = {"center": None, "data": []}

    def SetCenter(self, center):
        for k in range(self.K):
            self.Group[k]["center"] = center[k]

    def __distance(self, dat1, dat2):
        return abs(dat1-dat2)

    def SetData(self, data):
        self.data = data
        self.__update_date()
        self.pre_center = self.__get_center_vector()

    def __update_center(self):
        """
        更新中心
        """
        for k in range(self.K):
            _center = 0.0
            for i in self.Group[k]["data"]:
                _center += self.data[i]
            _center /= float(len(self.Group[k]["data"]))
            self.Group[k]["center"] = _center

    def __update_date(self):
        """
        根据中心设置数据
        """
        for k in range(self.K):
            self.Group[k]["data"] = []

        for i in range(len(self.data)):
            _group = None
            for k in range(self.K):
                distance = self.__distance(self.data[i], self.Group[k]["center"])
                if _group is None:
                    _group = (k, distance)
                    continue
                if distance < _group[1]:
                    _group = (k, self.__distance(self.data[i], self.Group[k]["center"]))
            self.Group[_group[0]]["data"].append(i)

    def __similarity(self, vector1, vector2):
        res = 0
        tmp0 = 0
        tmp1 = 0
        tmp2 = 0
        for i in range(len(vector1)):
            tmp0 += vector1[i]*vector2[i]
            tmp1 += pow(vector1[i], 2)
            tmp2 += pow(vector2[i], 2)

        res = float(tmp0)/(math.sqrt(tmp1)*math.sqrt(tmp2))
        return res

    def __get_center_vector(self):
        """
        获取聚类中心向量
        """
        res = []
        for k in range(self.K):
                res.append(self.Group[k]["center"])
        return res

    def Run(self):

        while True:
            self.__update_center()
            current_center = self.__get_center_vector()
            e = self.__similarity(current_center, self.pre_center)
            print e, current_center, self.pre_center
            if e > 0.99:
                return
            self.pre_center = current_center
            self.__update_date()


