#coding=utf8

''' 
字符切割
image=PIL.Image
灰度 0=黑 255=白
'''
import Image
import ImageDraw
#import numpy
#from scipy.optimize import leastsq
#import pylab
import Histogram
import ocr_normalize
import ocr_denoice_image

def BackgroundDistList(image,direction='h'):
    ''' (图像,方向=h or w)'''
    dist=[]
    width,height=image.size
    dist=[]
    pix=image.load()
    if direction=='h':
        for x in range(width):
            count=0
            for y in range(height):
                if pix[x,y]==0:
                    count+=1
            dist.append(count)
        return dist
    
    else:

        for y in range(height):
            count=0
            for x in range(width):
                if pix[x,y]==0:
                    count+=1
            dist.append(count)
    
        return dist


#---------------------------------------------------------------------------
def DistImage_H(hist):
    ''' 垂直方向脂肪图'''
    w=len(hist)
    h = 200

    print '-'*20
    myhist = Histogram.Histogram(hist)
    print myhist.getPeakPosition()


    hist = map(lambda i:h-h*i/max(hist),hist) #归一化,之后会有误差

    img = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(img)

    step = 1 # 每个矩形的宽度
    [draw.rectangle([i*step,hist[i],(i+1)*step,h],fill=0) for i in range(w)]

    return img


def DistImage_W(hist):
    ''' 水平方向的脂肪图'''
    w=200
    h=len(hist)

    print 'W-'*20
    myhist = Histogram.Histogram(hist)
    print myhist.getPeakPosition()

    hist = map(lambda i:w-w*i/max(hist),hist) #归一化,之后会有误差

    img = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(img)

    step = 1 # 每个矩形的宽度
    for i in range(h):
        draw.rectangle([(0,i*step),(w-hist[i],(i+1)*step)],fill=0)

    return img
#---------------------------------------------------------------------------

def DistImage(hist,direction='h'):
    """ 背景分布图
    (直方图)
    """
    if direction=='h':
        return DistImage_H(hist)
    else:
        #print hist
        return DistImage_W(hist)

#---------------------------------------------------------------------------
def get_block(image, x0, y0):
    checked = []
    get_next = [(x0, y0)]
    pix = image.load()
    width, height = image.size

    around = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    while len(get_next) > 0:
        tmp_get_next = []
        for x, y in get_next:
            checked.append((x, y))
            for x_, y_ in around:
                _x, _y = x+x_, y+y_
                if _x < 0 or _y < 0 or _x >= width or _y >= height:
                    continue

                if pix[_x, _y] > 0:
                    if (_x, _y) in checked:
                        continue
                    if (_x, _y) in tmp_get_next:
                        continue
                    tmp_get_next.append((_x, _y))

        get_next = tmp_get_next

    return checked


def GetWord(image, x, y, w, h):
    img = Image.new("L", (w, h), 0)
    pix_word = img.load()
    pix = image.load()

    for i in range(w):
        for j in range(h):
            pix_word[i, j] = pix[x+i, y+j]

    return img

#----------------------------------------------------------
def Segmentation(image):
    """分割图像
    """
    hist_value_H = BackgroundDistList(image, direction='h')
    hist_value_W = BackgroundDistList(image, direction='w')

    img = image.copy()
    width, height = img.size

    #纵向切割
    hist_h = Histogram.Histogram(hist_value_H)
    #横向切割
    hist_w = Histogram.Histogram(hist_value_W)

    peak_h = hist_h.getPeakPosition()
    peak_w = hist_w.getPeakPosition()

    im_list = []
    for i in range(len(peak_h)):
        for j in range(len(peak_w)):
            x, y = peak_h[i], peak_w[j]
            try:
                w = peak_h[i+1] - x
            except:
                w = width - x
            try:
                h = peak_w[j+1] - y
            except:
                h = height - y

            im = GetWord(img, x, y, w, h)
            im_list.append((im, (i, j)))

    draw = ImageDraw.Draw(img)
    for x in peak_h:
        draw.line((x, 0, x, height), fill=200)

    for y in peak_w:
        draw.line((0, y, width, y), fill=200)

    return img, im_list

#----------------------------------------------------------
