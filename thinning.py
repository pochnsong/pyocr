#coding=utf8
from thinning_table import table
import cv
import ImageTool


def VThin(image):
    img = image.copy()
    w, h = img.size
    pix = img.load()

    NEXT = 1
    for y in range(h):
        for x in range(w):
            if NEXT == 0:
                NEXT = 1
            else:
                M = pix[x-1, y]+pix[x, y]+pix[x+1, y] if 0 < x < w-1 else 1
                if pix[x, y] == 0 and M != 0:
                    a = [0]*9
                    for k in range(3):
                        for l in range(3):
                            if -1<(y-1+k)<h and -1<(x-1+l)<w and pix[x-1+l, y-1+k] == 255:
                                a[k*3+l] = 1
                    sum = a[0]*1+a[1]*2+a[2]*4+a[3]*8+a[5]*16+a[6]*32+a[7]*64+a[8]*128
                    pix[x, y] = table[sum]*255
                    if table[sum] == 1:
                        NEXT = 0
    return img


def HThin(image):
    img = image.copy()
    w, h = img.size
    pix = img.load()

    NEXT = 1
    for x in range(w):
        for y in range(h):
            if NEXT == 0:
                NEXT = 1
            else:
                M = pix[x, y-1]+pix[x,y]+pix[x, y+1] if 0 < y < h-1 else 1
                if pix[x, y] == 0 and M != 0:
                    a = [0]*9
                    for k in range(3):
                        for l in range(3):
                            if -1<(y-1+k)<h and -1<(x-1+l)<w and pix[x-1+l, y-1+k] == 255:
                                a[k*3+l] = 1
                    sum = a[0]*1+a[1]*2+a[2]*4+a[3]*8+a[5]*16+a[6]*32+a[7]*64+a[8]*128
                    pix[x, y] = table[sum]*255
                    if table[sum] == 1:
                        NEXT = 0
    return img


def ThinningImage(image, num=10):
    img = image.copy()

    w, h = img.size
    pix = img.load()

    for x in range(w):
        for y in range(h):
            if pix[x, y] == 0:
                pix[x, y] = 255
                continue

            pix[x, y] = 0


    for i in range(num):
        img = VThin(img)
        img = HThin(img)
    return img


