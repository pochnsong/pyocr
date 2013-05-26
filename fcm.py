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

#----------------------------------------------------------
class FCM_fast:
    def __init__(self, data, m=2, e=0.001):
        """
        data-分类数据,[(特征1,特征H(l),附加信息),(),()]
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
                dij = self.distance(self.c[i], self.data[j][0])
                if dij == 0:
                    self.u[i, j] = 1
                    continue

                for k in range(2):
                    tmp = dij/self.distance(self.c[k], self.data[j][0])
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
                tmp1 += pow(self.u[i, j], self.m)*self.data[j][0]*self.data[j][1]
                pass
            for j in range(len(self.data)):
                tmp2 += pow(self.u[i, j], self.m)*self.data[j][1]
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
                tmp = float(pow(self.u[i, j], self.m))
                tmp *= float(pow(self.distance(self.c[i], self.data[j][0]), 2))
                tmp *= self.data[j][1]
                res += tmp
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

#----------------------------------------------------------
class FCM_image:
    def __init__(self, img, m=2, e=0.001, NB=9):
        """
        data-分类数据,[(特征1,特征H(l),附加信息),(),()]
        c-分类数,
        m-加权指数,
        e-误差
        NB-滑动窗口
        M,N 图像尺寸
        """
        self.img =img
        self.pix = img.load()
        self.m = m
        self.e = e
        self.NB = NB
        self.W, self.H = img.size

        return

    def similarity(self, x1, x2):
        """
        x_ik,x_ij 灰度值
        """
        return 1.0/(1.0+abs(x1-x2))

    def get_window_pix(self, x, y):
        """
        获取第k个数据的窗口象素
        """
        r = (self.NB-1)/2 #半径
        #滑动窗口包含的像素点
        window_pix_list = []
        for i in range(self.NB):
            for j in range(self.NB):
                _x, _y = x-r+i, y-r+j

                try:
                    tmp = self.pix[_x, _y]
                    window_pix_list.append((_x, _y))
                except Exception,e:
                    #print "window:",(x, y),(_x, _y),e,self.img.size,r,i,j
                    continue

        window_pix_list.remove((x, y))
        return window_pix_list

    def uk(self, x, y):
        """
        计算滑动窗口中心象素点x,y和其余个点平均相似度
        """

        res = 0
        #滑动窗口包含的像素点
        window_pix_list = self.get_window_pix(x, y)
        for _x, _y in window_pix_list:
            res += self.similarity(self.pix[x, y], self.pix[_x, _y])

        try:
            res /= len(window_pix_list)
        except:
            print x, y
            exit()

        return res

    def Uik_(self, i, x, y):
        """
        第i类
        第k个数据
        """
        return self.uik[i, x, y]*self.Uk[x, y]

    def hik(self, i, x, y):
        """
        空间邻域函数
        k = x, y
        """
        res = 0
        r = (self.NB-1)/2 #半径
        #pos_start = x-r, y-r
        #滑动窗口包含的像素点
        window_pix_list = self.get_window_pix(x, y)
        for x, y in window_pix_list:
            res += self.uik_[i, x, y]

        return res

    def distance(self, d1, d2):

        return float(abs(d1-d2))

    def _U_fast(self):
        """
        计算划分矩阵
        """
        self.ul = {}
        for i in range(2):
            for j in range(len(self.data)):
                self.ul[i, j] = 0
                for k in range(2):
                    tmp = self.distance(self.c[i], self.data[j][0])/self.distance(self.c[k], self.data[j][0])
                    self.ul[i, j] += pow(tmp, (2.0/(self.m-1)))
                    pass
                self.ul[i, j] = 1.0 / self.ul[i, j]
                pass
            pass
        pass


    def _U(self):
        """
        计算划分矩阵
        """
        self._U_fast()
        self.uik = {}
        for i in range(len(self.data)):
            for x, y in self.gray_hist_pix[i]:
                self.uik[0, x, y] = self.ul[0, i]
                self.uik[1, x, y] = self.ul[1, i]

        self.uik_ = {}
        for i in range(2):
            for x in range(self.W):
                for y in range(self.H):
                    self.uik_[i, x, y] = self.Uik_(i, x, y)


        self.Hik = {}

        for i in range(2):
            for x in range(self.W):
                for y in range(self.H):
                    self.Hik[i, x, y] = self.hik(i, x, y)

        self.u = {}
        for i in range(2):
            print "_U", i
            for x in range(self.W):
                for y in range(self.H):

                    self.u[i, x, y] = self.uik_[i, x, y]*self.Hik[i, x, y]
                    self.u[i, x, y] = self.uik_[i, x, y]

                    tmp = 0
                    for j in range(2):
                        tmp += self.uik_[j, x, y]*self.Hik[j, x, y]
                        #tmp += self.uik_[j, x, y]
                        #print "tmp:", tmp, (x, y)
                        pass
                    self.u[i, x, y] = self.u[i, x, y]/tmp

    def _C(self):
        """
        计算分类中心
        """
        for i in range(2):
            tmp1 = 0
            tmp2 = 0
            for x in range(self.W):
                for y in range(self.H):
                    tmp = pow(self.u[i, x, y], self.m)
                    tmp1 += tmp*self.pix[x, y]
                    tmp2 += tmp

            self.c[i] = float(tmp1)/float(tmp2)

        return

    def sim(self):
        """
        计算像素窗口相似度
        """
        print "计算像素的邻域相似度"
        self.Uk = {}
        for x in range(self.W):
            for y in range(self.H):
                self.Uk[x, y] = self.uk(x, y)

    def start(self):
        """
        初始化聚类中心,使用快速聚类
        """
        gray_hist = [0]*256
        self.gray_hist_pix = [[] for i in range(256)]

        for x in range(self.W):
            for y in range(self.H):
                gray_hist[self.pix[x, y]] += 1
                self.gray_hist_pix[self.pix[x, y]].append((x, y))

        self.data = []
        for l in range(len(gray_hist)):
            self.data.append((l, gray_hist[l]))

        ff = FCM_fast(self.data)
        ff.Run()
        self.c = ff.c
        self.sim()
        self._U()
        return

    def J(self):
        """
        """
        res = 0
        for i in range(2):
            for x in range(self.W):
                for y in range(self.H):
                    tmp = float(pow(self.u[i, x, y], self.m))
                    tmp *= float(pow(self.distance(self.c[i], self.pix[x, y]), 2))
                    res += tmp

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

