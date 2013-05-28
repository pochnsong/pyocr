#coding=utf8
__author__ = 'song'

import wx
from wx import xrc
import frame_xrc
import ImageTool
import ocr_normalize
import ocr_segmentation_image
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
        self.il = wx.ImageList(200, 200, True)
        for im, info in word_list:
            try:
                img = ImageTool.pilImage_to_wxImage(im)
            except:
                print im, im.size, info
            bmp = wx.BitmapFromImage(img)
            self.il.Add(bmp)

        # create the list control
        #创建列表窗口部件
        self.list = xrc.XRCCTRL(self, "img_list_ctrl")

        # assign the image list to it
        self.list.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)

        # create some items for the list
        #为列表创建一些项目
        for x in range(len(word_list)):
            img_index = x
            name = str(word_list[x][1])
            self.list.InsertImageStringItem(x, name, img_index)

        self.BindEvent()

    def OnGetSide1(self, event):
        img_list = []
        for im, info in self.word_list:
            _x, _y, x_, y_ = ocr_normalize.GetWordSide1(im)
            #img = im.copy()
            try:
                img = ocr_segmentation_image.GetWord(im, _x, _y, x_-_x, y_-_y)
            except:
                print info, im.size, _x, _y, x_, y_
                continue
                #exit()
            draw = ImageDraw.Draw(im)
            draw.line((_x, _y, _x, y_), fill=100)
            draw.line((_x, _y, x_, _y), fill=100)
            draw.line((x_, y_, _x, y_), fill=100)
            draw.line((x_, y_, x_, _y), fill=100)

            hist_im = im.histogram()[255]
            hist_img = img.histogram()[255]
            if hist_im == 0:
                continue
            else:
                percent = 1.0 - float(hist_im-hist_img)/float(hist_im)

            img_list.append((img, percent))

        word_side_frame = WordListFrame(img_list)
        word_side_frame.Show()


