#coding=utf8
''' 
处理有关图像的操作

'''
import Image
def Scale(image,rate):
    ''' 图像缩放(图像,比率)'''

    w,h=image.size

    return image.resize((int(w*rate),int(h*rate)),Image.ANTIALIAS)
