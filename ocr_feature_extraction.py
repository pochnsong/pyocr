#coding=utf8
__author__ = 'song'
"""
特征提取
对象：单个文字图像PIL Image类型
图像大小为 24*24
"""

import ocr_normalize

def get_outside_feature(image):
    """
    粗外围特征提取
    """
    n = 8
    width, height = image.size
    pix = image.load()
    w = width/8

    feature_left = []
    # 左边框特征
    for i in range(n):
        I = 0
        for y in range(i*w, w*(i+1)):
            for x in range(width):
                if pix[x, y] == 255:
                    break
                I += 1
        feature_left.append(I)

    feature_right = []
    # 右边框特征
    for i in range(n):
        I = 0
        for y in range(i*w, w*(i+1)):
            for x in range(width-1, -1, -1):

                if pix[x, y] == 255:
                    break
                I += 1
        feature_right.append(I)

    feature_top = []
    # 上边框特征
    for i in range(n):
        I = 0
        for x in range(i*w, w*(i+1)):
            for y in range(height):
                if pix[x, y] == 255:
                    break
                I += 1
        feature_top.append(I)

    feature_bottom = []
    # 上边框特征
    for i in range(n):
        I = 0
        for y in range(i*w, w*(i+1)):
            for x in range(width-1, -1, -1):
                if pix[x, y] == 255:
                    break
                I += 1
        feature_bottom.append(I)

    return [feature_right, feature_left, feature_top, feature_bottom]


def get_outside_feature2(image):
    """
    粗外围特征提取
    """
    n = 8
    width, height = image.size
    pix = image.load()
    w = width/8

    feature_left = []
    feature_right = []

    # 左边框特征
    # 右边框特征

    for y in range(height):
        I = 0
        for x in range(width):
            if pix[x, y] > 0:
                break
            I += 1
        feature_left.append(I)

        I = 0
        for x in range(width-1, -1, -1):
            if pix[x, y] > 0:
                break
            I += 1
        feature_right.append(I)

    feature_top = []
    feature_bottom = []

    # 上下边框特征
    for x in range(width):
        I = 0
        for y in range(height):
            if pix[x, y] == 255:
                break
            I += 1
        feature_top.append(I)

        I = 0
        for y in range(height-1, -1, -1):
            if pix[x, y] == 255:
                break
            I += 1
        feature_bottom.append(I)

    return [feature_right, feature_left, feature_top, feature_bottom]


def get_outside_feature3(image):
    """
    粗外围特征提取 比例
    """
    n = 8
    width, height = image.size
    center_x, center_y = ocr_normalize.GetCenterPos(image)
    pix = image.load()
    w = width/8

    feature_left = []
    feature_right = []

    # 左边框特征
    # 右边框特征

    for y in range(height):
        I = 0
        for x in range(center_x):
            if pix[x, y] > 0:
                break
            I += 1
        I = float(I)/float(center_x)
        feature_left.append(I)

        I = 0
        for x in range(width-1, center_x, -1):
            if pix[x, y] > 0:
                break
            I += 1
        I = float(I)/float(center_x)
        feature_right.append(I)

    feature_top = []
    feature_bottom = []

    # 上下边框特征
    for x in range(width):
        I = 0
        for y in range(center_y):
            if pix[x, y] == 255:
                break
            I += 1
        I = float(I)/float(center_y)
        feature_top.append(I)

        I = 0
        for y in range(height-1, center_y, -1):
            if pix[x, y] == 255:
                break
            I += 1
        I = float(I)/float(center_y)
        feature_bottom.append(I)


    return [feature_right, feature_left, feature_top, feature_bottom]
