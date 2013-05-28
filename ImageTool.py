#coding=utf8

import cv
from PIL import Image
import wx

def wxImage_to_pilImage(image):
    """Convert wx.Image to PIL Image."""
    pil = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil.fromstring(image.GetData())
    return pil

def pilImage_to_wxImage(pil, alpha=True):
    """Convert PIL Image to wx.Image."""
    if alpha:
        image = apply(wx.EmptyImage, pil.size)
        image.SetData(pil.convert("RGB").tostring())
        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
    return image

def PIL2cvmat (im):
    cv_im = cv.CreateImageHeader(im.size, cv.IPL_DEPTH_8U, 3)
    cv.SetData(cv_im, im.tostring())
    bgr = cv.CloneImage(cv_im)
    cv.CvtColor( cv_im, bgr, cv.CV_RGB2BGR )
    return cv.GetMat(bgr)

def cvmat2PIL (cv_im):
    rgb = cv.CloneMat(cv_im)
    cv.CvtColor(cv_im, rgb, cv.CV_BGR2RGB)
    im = Image.fromstring("RGB", cv.GetSize(rgb), rgb.tostring())
    return im


