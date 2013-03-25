#coding=utf8

''' 
字符切割
image=PIL.Image
灰度 0=黑 255=白
'''
import Image
import ImageDraw

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
    h=200
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
    hist = map(lambda i:w-w*i/max(hist),hist) #归一化,之后会有误差

    img = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(img)

    step = 1 # 每个矩形的宽度
    for i in range(h):
        draw.rectangle([(0,i*step),(w-hist[i],(i+1)*step)],fill=0)

    return img
#---------------------------------------------------------------------------
def DistImage(hist,direction='h'):
    ''' 背景分布图
    (直方图)
    '''
    if direction=='h':
        return DistImage_H(hist)
    else:
        #print hist
        return DistImage_W(hist)
        
