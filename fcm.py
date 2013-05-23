#coding=utf8
__author__ = 'song'
import math

class FCM_normal:
    def __init__(self, data, m=2, e=0.001):
        """
        data-分类数据,[(特征,附加信息),(),()]
        c-分类数,
        m-加权指数,
        e-误差
        """
        self.data = data
        self.m = m
        self.e = e
        return

    def distance(self, d1, d2):

        return float(abs(d1-d2))

    def _U(self):
        """
        计算划分矩阵
        """
        self.u = {}
        for i in range(2):
            for j in range(len(self.data)):
                self.u[i, j] = 0
                for k in range(2):
                    tmp = self.distance(self.c[i], self.data[j][0])/self.distance(self.c[k], self.data[j][0])
                    self.u[i, j] += pow(tmp, (2.0/(self.m-1)))
                    pass
                self.u[i, j] = 1.0 / self.u[i, j]
                pass
            pass
        pass

    def _C(self):
        """
        计算分类中心
        """
        for i in range(2):
            tmp1 = 0
            tmp2 = 0
            for j in range(len(self.data)):
                tmp1 += pow(self.u[i, j], self.m)*self.data[j][0]
                pass
            for j in range(len(self.data)):
                tmp2 += pow(self.u[i, j], self.m)
                pass

            self.c[i] = float(tmp1)/float(tmp2)
            pass

        return

    def start(self):
        """
        初始化聚类中心,
        """
        self.c = [0.5, 255.5]
        self._U()
        return

    def J(self):
        """
        """
        res = 0
        for i in range(2):
            for j in range(len(self.data)):
                res += float(pow(self.u[i, j], self.m))*float(pow(self.distance(self.c[i], self.data[j][0]), 2))
                pass
            pass

        return res

    def Run(self):
        """
        标准fcm算法
        """
        self.counter = 1 #计数器
        self.start()

        while True:
            print "c:", self.c
            self.pre_J = self.J()

            self._U()
            self._C()
            tmp_J = self.J()

            if abs(tmp_J-self.pre_J) < self.e:
                break

            self.pre_J = tmp_J
            self.counter += 1

        return

