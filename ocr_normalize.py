#coding=utf8
__author__ = 'song'

import ocr_segmentation

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
            _x = x+1
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
            x_ = x-1
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
            _y = y+1
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
            y_ = y-1
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

    return _x, _y, x_, y_


def ModifyWordSide(image, _x, _y , x_ ,y_):
    """
    修正文字边框
    image 总体文字图片
    _x, _y, x_, y_ 当前的文字边框
    """
    img = image.copy()
    W, H = img.size
    pix = img.load()

    #im = ocr_segmentation.GetWord(image, _x, _y, x_-_x, y_-_y)

    left = 0
    for x in range(0, _x):
        for y in range(H):
            if pix[x, y] > 0:
                left += 1

    right = 0
    for x in range(x_, W):
        for y in range(H):
            if pix[x, y] > 0:
                right += 1
    top = 0
    for y in range(0, _y):
        for x in range(W):
            if pix[x, y] > 0:
                top += 1

    bottom = 0
    for y in range(y_, H):
        for x in range(W):
            if pix[x, y] > 0:
                bottom += 1

    print "L:R:T:B",left, right, top, bottom

    if left == max(right, left, top, bottom):
        start = False
        y_list = [_y, y_]
        find = False
        for x in range(_x-1, -1, -1):
            for y in range(H):
                if pix[x, y] > 0:
                    find = True
                    _x = x
                    break
            if find:
                break
        print "L:",_x
        for x in range(_x-1, -1, -1):
            find = False
            for y in range(H):
                if pix[x, y] > 0:
                    find = True
                    _x = x
                    if y not in y_list:
                        y_list.append(y)
            if not find:
                break

        print "L----"
        return _x, min(y_list), x_, max(y_list)

    if right == max(right, left, top, bottom):
        start = False
        y_list = [_y, y_]
        find = False
        for x in range(x_+1, W):
            for y in range(H):
                if pix[x, y] > 0:
                    find = True
                    x_ = x
                    break
            if find:
                break

        for x in range(x_+1, W):
            find = False
            for y in range(H):
                if pix[x, y] > 0:
                    find = True
                    x_ = x
                    if y not in y_list:
                        y_list.append(y)
            if not find:
                break

        print "R----"
        return _x, min(y_list), x_, max(y_list)

    if top == max(right, left, top, bottom):
        x_list = [_x, x_]
        find = False
        for y in range(_y-1, -1, -1):
            for x in range(W):
                if pix[x, y] > 0:
                    find = True
                    _y = y
                    break
            if find:
                break

        for y in range(_y-1, -1, -1):
            find = False
            for x in range(W):
                if pix[x, y] > 0:
                    find = True
                    _y = y
                    if x not in x_list:
                        x_list.append(y)
            if not find:
                break

        print "T----"
        return min(x_list), _y, max(x_list), y_

    if bottom == max(right, left, top, bottom):
        x_list = [_x, x_]
        find = False
        for y in range(y_+1, H):
            for x in range(W):
                if pix[x, y] > 0:
                    find = True
                    y_ = y
                    break
            if find:
                break

        for y in range(y_+1, H):
            find = False
            for x in range(W):
                if pix[x, y] > 0:
                    find = True
                    y_ = y
                    if x not in x_list:
                        x_list.append(y)
            if not find:
                break

        print "B----"
        return min(x_list), _y, max(x_list), y_


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