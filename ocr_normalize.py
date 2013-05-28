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
        for x in range(sx, W):
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
        for x in range(sx, -1, -1):
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
        for y in range(sy, H):
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

    draw = Image
    for _x, _y in center_list:
        draw.line(_x, fill=255)
        draw.line(_y, fill=255)

    for x in peak_h:
        draw.line((x, 0, x, height), fill=128)

    for y in peak_w:
        draw.line((0, y, width, y), fill=128)

    for im, xs, ys in im_list:
        _x, _y, x_, y_ = ocr_normalize.GetWord1(im)
        _x, _y, x_, y_ = _x+xs, _y+ys, x_+xs, y_+ys
        w, h = im.size
        draw.line((_x, _y, _x, y_), fill=50)
        draw.line((_x, _y, x_, _y), fill=100)
        draw.line((x_, y_, _x, y_), fill=150)
        draw.line((x_, y_, x_, _y), fill=200)

        cx, cy = ocr_normalize.GetCenterPos(im)
        _cx = int(cx-w*0.1)
        if _cx < 0:
            _cx = 0
        cx_ = int(cx+w*0.1)
        if cx_ > w-1:
            cx_ = w-1
        _cy = int(cy-h*0.1)
        if _cy < 0:
            _cy = 0
        cy_ = int(cy+h*0.1)
        if cy_ > h-1:
            cy_ = h-1
        _cx, _cy, cx_, cy_ = _cx+xs, _cy+ys, cx_+xs, cy_+ys
        draw.line((_cx, _cy, _cx, cy_), fill=255)
        draw.line((_cx, _cy, cx_, _cy), fill=255)
        draw.line((cx_, cy_, _cx, cy_), fill=255)
        draw.line((cx_, cy_, cx_, _cy), fill=255)
    """
    pass