#coding=utf8
""" 
本模块所有的image类型都为PIL.Image
"""


from ImageTool import *
import Image
import ImageDraw

def ConvertImage(image):
    ''' 把彩色图像转换成灰度图像
    image=PIL.Image
    return PIL.Image
    '''

    return image.convert("L")

def HistogramImage(image, w=512, h=256):
    ''' 获取灰度直方图
    image=灰度图像
    '''
    image=image.convert("L")

    hist = image.histogram()
    hist = map(lambda i:h-h*i/max(hist),hist) #归一化,之后会有误差

    w=w%256 and 256*(w/256+1) or w #保证宽是256的倍数

    img = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(img)

    step = w/256 # 每个矩形的宽度
    [draw.rectangle([i*step,hist[i],(i+1)*step,h],fill=0) for i in range(256)]

    return img

def GetThreshold(image):
    ''' 获取阈值'''
    histogram=image.histogram() #获取灰度直方图

    g1=[0,histogram[0]]
    for i in range(0,127):
        if histogram[i]>g1[1]:
            g1=[i,histogram[i]]

    g2=[127,histogram[127]]
    for i in range(127,255):
        if histogram[i]>g2[1]:
            g2=[i,histogram[i]]

    threshold=int((g1[0]+g2[0])/2)
    return threshold

def BinaryImage(image,threshold=0):
    """ 
    PIL图像,阈值=0自动
    wximage(PIL.Image),threshold(0~255)

    return image=PIL.Image
    """
    
    #
    if threshold==0:
        threshold=GetThreshold(image)
            
    img=image.copy()
    width,height=img.size
    pix=img.load()
    for w in range(width):
        for h in range(height):
            if pix[w,h]>threshold:
                pix[w,h]=255
            else:
                pix[w,h]=0
                
    return img
