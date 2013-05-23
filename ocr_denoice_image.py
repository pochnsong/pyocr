#coding=utf8

import ImageFilter
import fcm

def MedianFilter(image,size=3):
    '''
    图像去噪
    采用中值滤波
    медианный фильтр median filter
    '''
    return image.filter(ImageFilter.MedianFilter(size))

def DenoiceImage(image):
    '''
    图像去噪
    采用中值滤波
    медианный фильтр median filter
    '''
    median_filter=ImageFilter.MedianFilter()
    return median_filter.filter(image)

def Denoice_FCM_Normal(image):
    """
    图像去噪
    常规FCM
    """
    img = image.copy()
    pix = img.load()

    width, height = img.size

    dat = []
    for x in range(width):
        for y in range(height):
            dat.append((pix[x, y], (x, y)))


    f1 = fcm.FCM_normal(dat)
    f1.Run()
    print f1.counter
    print f1.J()

    for i in range(len(dat)):
        x, y = dat[i][1]
        if f1.u[1, i] > f1.u[0, i]:
            pix[x, y] = 255
        else:
            pix[x, y] = 0

    return img


