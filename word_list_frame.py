#coding=utf8
__author__ = 'song'

import wx
from wx import xrc
import frame_xrc
import ImageTool
import ocr_normalize
from PIL import ImageDraw

class WordListFrame(frame_xrc.xrcWordList):
    def BindEvent(self):
        self.Bind(wx.EVT_MENU, self.OnGetSide1, id=xrc.XRCID("menu_find_side1"))

    def __init__(self, word_list):
        frame_xrc.xrcWordList.__init__(self, None)
        # load some images into an image list
        #创建图像列表
        self.word_list = word_list
        w, h = word_list[0][0].size
        self.il = wx.ImageList(w, h, True)
        for im, _x, _y in word_list:
            #im.save(str(_x)+str(_y)+".png")
            img = ImageTool.pilImage_to_wxImage(im)
            bmp = wx.BitmapFromImage(img)
            il_max = self.il.Add(bmp)

        # create the list control
        #创建列表窗口部件
        self.list = xrc.XRCCTRL(self, "img_list_ctrl")

        # assign the image list to it
        self.list.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)

        # create some items for the list
        #为列表创建一些项目
        for x in range(self.il.GetImageCount()):
            img = x % (il_max+1)
            self.list.InsertImageStringItem(x,
                    "%02d" % x, img)

        self.BindEvent()

    def OnGetSide1(self, event):
        img_list = []
        for im, i, j in self.word_list:
            _x, _y, x_, y_ = ocr_normalize.GetWordSide1(im)
            img = im.copy()
            draw = ImageDraw.Draw(img)
            draw.line((_x, _y, _x, y_), fill=100)
            draw.line((_x, _y, x_, _y), fill=100)
            draw.line((x_, y_, _x, y_), fill=100)
            draw.line((x_, y_, x_, _y), fill=100)
            img_list.append((img, i, j))
            if im.histogram()[255] == 0:
                print (i, j), 0
            else:
                print (i, j), float(img.histogram()[255])/float(im.histogram()[255])

        word_side_frame = WordListFrame(img_list)
        word_side_frame.Show()
