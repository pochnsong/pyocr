#coding=utf8

import ImageFilter
import fcm
import kmeans


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


def Denoice_FCM_Fast(image):
    """
    图像去噪
    常规FCM
    """
    img = image.copy()
    width, height = img.size

    gray_hist = [0]*256
    gray_hist_pix = [[] for i in range(256)]
    pix = img.load()

    for x in range(width):
        for y in range(height):
            gray_hist[pix[x, y]] += 1
            gray_hist_pix[pix[x, y]].append((x, y))
            #print pix[x, y], len(gray_hist_pix[pix[x, y]])

    dat = []
    for l in range(len(gray_hist)):
        dat.append((l, gray_hist[l]))


    f1 = fcm.FCM_fast(dat)
    f1.Run()
    print f1.counter
    print f1.J()

    print len(gray_hist_pix[127]), width*height

    for i in range(len(dat)):
        if f1.u[1, i] > f1.u[0, i]:
            for pos in gray_hist_pix[i]:
                pix[pos] = 255
        else:
            for pos in gray_hist_pix[i]:
                pix[pos] = 0

    return img


def Denoice_FCM_block(image):

    img = image.copy()
    pix = img.load()

    f1 = fcm.FCM_image(img)
    f1.Run()

    width, height = img.size
    for x in range(width):
        for y in range(height):
            if f1.u[0, x, y] > f1.u[1, x, y]:
                pix[x, y] = 0
            else:
                pix[x, y] = 255

    return img



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

def Get_Block(image):
    """
    获取image的block
    """
    img = image.copy()
    width, height = img.size
    pix = img.load()
    block_list = []
    checked = []

    for x in range(width):
        for y in range(height):
            if pix[x, y] > 0:
                if (x, y) in checked:
                    continue
                block = get_block(img, x, y)
                checked += block
                block_list.append((len(block),block))
    f1 = fcm.FCM_normal(block_list)
    f1.Run()
    for i in range(len(block_list)):
        if f1.u[1, i] < f1.u[0, i]:
            for x, y in block_list[i][1]:
                pix[x, y] = 0

    return img


def Denoise_kmeans(image):
    img = image.copy()
    width, height = img.size
    pix = img.load()
    block_list = []
    data = []
    checked = []

    print "Get Block"
    for x in range(width):
        for y in range(height):
            if pix[x, y] > 0:
                if (x, y) in checked:
                    continue
                block = get_block(img, x, y)
                checked += block
                data.append(len(block))
                block_list.append(block)

    print "数据长度:", len(data)
    k1 = kmeans.KMeans(2)
    k1.SetCenter([1,100])
    k1.SetData(data)
    k1.Run()

    for i in k1.Group[0]["data"]:
        for x, y in block_list[i]:
            pix[x, y] = 0

    return img
