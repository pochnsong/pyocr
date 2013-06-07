#coding=utf8

import ImageFilter
import fcm
import kmeans
import ocr_segmentation

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
                block = ocr_segmentation.get_block(img, x, y)
                checked += block
                data.append(len(block))
                block_list.append(block)

    print "数据长度:", len(data)
    k1 = kmeans.KMeans(3)
    k1.SetCenter([1, 20, 100])
    k1.SetData(data)
    k1.Run()

    for i in k1.Group[0]["data"]:
        for x, y in block_list[i]:
            pix[x, y] = 0

    return img


def Denoise_kmeans_fast(image):

    image_block = image.copy()
    pix_image_block = image_block.load()

    width, height = image_block.size
    block_list = []
    data = []

    print "Get Block"
    for x in range(width):
        for y in range(height):
            if pix_image_block[x, y] > 0:
                #print "before:",(x, y),image_block.histogram()[255]
                #print "id:",id(pix_image_block)
                block = ocr_segmentation.get_block_fast(pix_image_block, x, y, width, height)
                #print "after:", image_block.histogram()[255],len(block)
                #sss = raw_input()
                data.append(len(block))
                block_list.append(block)

    print "数据长度:", len(data)

    k1 = kmeans.KMeans(3)
    k1.SetCenter([1, 20, 100])
    k1.SetData(data)
    k1.Run()

    img = image.copy()
    pix = img.load()

    for i in k1.Group[0]["data"]:
        for x, y in block_list[i]:
            pix[x, y] = 0

    return img

def RemoveBlankBorder(image):
    """
    删除整体图像边界处留白
    """
    img = image.copy()
    width, height = img.size
    pix = img.load()
    #处理左边界
    for y in range(height):
        ocr_segmentation.get_block_fast(pix, 0, y, width, height)
        ocr_segmentation.get_block_fast(pix, width-1, y, width, height)

    for x in range(width):
        ocr_segmentation.get_block_fast(pix, x, 0, width, height)
        ocr_segmentation.get_block_fast(pix, x, height-1, width, height)

    return img
