#coding=utf8
__author__ = 'song'


def GetCenterPos(image):
    """
    获取文字重心
    """
    W, H = image.size
    pix = image.load()
    tmpx = 0
    tmpy = 0
    tmp1 = 0

    for x in range(W):
        for y in range(H):
            tmpx += x*pix[x, y]
            tmpy += y*pix[x, y]
            tmp1 += pix[x, y]

    if tmp1 == 0:
        return W/2, H/2

    return tmpx/tmp1, tmpy/tmp1


def GetWordSide(image):
    """
    获取文字
    """
    W, H = image.size
    pix = image.load()
    _x, _y = 0, 0
    x_, y_ = 0, 0
    find = False
    for x in range(W):
        if find:
            break
        for y in range(H):
            if pix[x, y] > 0:
                _x = x
                find = True
                break

    find = False
    for y in range(H):
        if find:
            break
        for x in range(W):
            if pix[x, y] > 0:
                _y = y
                find = True
                break

    find = False
    for x in range(W-1, -1, -1):
        if find:
            break
        for y in range(H):
            if pix[x, y] > 0:
                x_ = x
                find = True
                break

    find = False
    for y in range(H-1, -1, -1):
        if find:
            break
        for x in range(W):
            if pix[x, y] > 0:
                y_ = y
                find = True
                break

    return _x, _y, x_, y_


def GetWordSide1(image):
    """
    获取文字1
    """
    W, H = image.size
    pix = image.load()

    #获取重心
    cx, cy = GetCenterPos(image)

    _x, _y = 0, 0
    x_, y_ = W, H

    sx = int(cx-W*0.1)
    if sx < 0:
        sx = 0

    #寻找左边
    find = False
    for x in range(sx, -1, -1):
        find = False
        for y in range(H):
            if pix[x, y] > 0:
                find = True
                break
        if not find:
            _x = x
            find = True
            break

    if not find:
        find = False
        for x in range(sx, cx):
            if find:
                break
            for y in range(H):
                if pix[x, y] > 0:
                    _x = x
                    find = True
                    break

    #寻找右边
    sx = int(cx+W*0.1)
    if sx > W-1:
        sx = W-1
    find = False
    for x in range(sx, W):
        find = False
        for y in range(H):
            if pix[x, y] > 0:
                find = True
                break
        if not find:
            #找到空白行
            x_ = x
            find = True
            break

    if not find:
        find = False
        for x in range(sx, cx, -1):
            for y in range(H):
                if pix[x, y] > 0:
                    x_ = x
                    find = True
                    break
            if find:
                break

    #寻找上边
    sy = int(cy-H*0.1)
    if sy < 0:
        sy = 0
    find = False
    for y in range(sy, -1, -1):
        find = False
        for x in range(W):
            if pix[x, y] > 0:
                find = True
                break
        if not find:
            _y = y
            find = True
            break

    if not find:
        find = False
        for y in range(sy, cy):
            if find:
                break
            for x in range(W):
                if pix[x, y] > 0:
                    _y = y
                    find = True
                    break
    #寻找下边
    sy = int(cy+H*0.1)
    if sy > H-1:
        sy = H-1
    find = False
    for y in range(sy, H):
        find = False
        for x in range(W):
            if pix[x, y] > 0:
                find = True
                break
        if not find:
            y_ = y
            find = True
            break

    if not find:
        for y in range(sy, cy, -1):
            if find:
                break
            for x in range(W):
                if pix[x, y] > 0:
                    y_ = y
                    find = True
                    break

    return _x+1, _y+1, x_-1, y_-1


def GetWordImage(image):
    """
    获取文字
    """
    hist_image = image.histogram()[255]
    if hist_image == 0:
        return None

    _x, _y, x_, y_ = GetWordSide1(image)

    try:
        img = image.crop(_x, _y, _x, _y)
    except:
        print image.size, _x, _y, x_, y_
        return None

    hist_img = img.histogram()[255]

    percent = 1.0 - float(hist_image-hist_img)/float(hist_image)

    pass