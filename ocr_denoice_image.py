#coding=utf8

import ImageFilter

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

