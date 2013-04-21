#coding=utf8
__author__ = 'jjdl'

import numpy
import pylab
from scipy.optimize import leastsq


def func(x, p):
    """
    数据拟合所用的函数: A*sin(2*pi*k*x + theta)
    """
    A, w, b = p
    return A*numpy.cos(w*x)+b


def residuals(p, y, x):
    """
    实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
    """
    return y - func(x, p)

class Histogram:
    """
    处理直方图
    """
    def __init__(self, hist):
        self.histdata = hist
        self.Init()
        return

    def getSize(self):

        x, y = len(self), 0

        for i in self.histdata:
            if i > y:
                y = i

        return x, y

    def Init(self):
        """
        获取周期数量
        """
        w = len(self.histdata)
        A = max(self.histdata)-min(self.histdata)

        k = 1
        #最小误差
        e_min_k=k
        e_min_plsq = None
        e_min = None
        #最小误差保持度
        e_count = 0

        while True:
            xn = numpy.linspace(0, k*2*numpy.pi, w)
            #函数
            plsq = leastsq(residuals, [A, 1, 0], args=(self.histdata, xn))

            e = 0
            _a, _w, b = plsq[0]
            #计算当前函数误差
            for i in range(w):
                fn_y = func(xn[i], plsq[0])-b
                _e = (self.histdata[i]-b)-fn_y
                e += _e*_e

            if e_min is None:
                e_min = e
                e_count = 0
                e_min_k = k
                e_min_plsq = plsq
            else:
                if e < e_min:
                    e_min = e
                    e_count = 0
                    e_min_k = k
                    e_min_plsq = plsq

                else:
                    e_count += 1

            if e_count > 5:
                self.plsq = e_min_plsq[0]
                self.k = e_min_k
                return

            k += 1
            pass


    def getPeakPosition(self):
        """
        获取峰值
        """
        res = []
        pre_value = None
        fn_direction = "+"

        xn = numpy.linspace(0, self.k*2*numpy.pi, len(self.histdata))
        for i in range(len(self.histdata)):
            fn_value = func(xn[i], self.plsq)
            if pre_value is None:
                pre_value = fn_value
                continue

            if fn_value > pre_value:
                fn_direction = "+"

            elif fn_value < pre_value:
                if fn_direction == "+":
                    res.append(i-1)
                fn_direction = "-"
            pre_value = fn_value

        print '---',res
        return res
