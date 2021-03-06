#coding=utf8
__author__ = 'song'

import wx
from wx import xrc
import frame_xrc
import ImageTool
import ocr_normalize
import ocr_segmentation
import thinning
from PIL import ImageDraw
import ocr_feature_extraction
import ocr_match

class WordListFrame(frame_xrc.xrcWordList):
    def BindEvent(self):
        self.Bind(wx.EVT_MENU, self.OnGetSide0, id=xrc.XRCID("menu_find_side0"))
        self.Bind(wx.EVT_MENU, self.OnGetSide1, id=xrc.XRCID("menu_find_side1"))
        self.Bind(wx.EVT_MENU, self.OnGetSide2, id=xrc.XRCID("menu_find_side2"))
        self.Bind(wx.EVT_MENU, self.OnResize, id=xrc.XRCID("menu_resize"))
        self.Bind(wx.EVT_MENU, self.OnThinning, id=xrc.XRCID("menu_thinning"))
        self.Bind(wx.EVT_MENU, self.OnMatch1, id=xrc.XRCID("menu_match_od"))

    def __init__(self, word_list):
        frame_xrc.xrcWordList.__init__(self, None)
        # load some images into an image list
        #创建图像列表
        self.word_list = word_list

        self.il = wx.ImageList(200, 200, True)
        for im, info in word_list:
            try:
                img = ImageTool.pilImage_to_wxImage(im)
            except:
                print im, im.size, info
                continue
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

    def OnGetSide0(self, event):
        img_list = []
        for im, info in self.word_list:
            hist_im = im.histogram()[255]
            if hist_im == 0:
                continue

            _x, _y, x_, y_ = ocr_normalize.GetWordSide(im)
            #img = im.copy()
            try:
                img = ocr_segmentation.GetWord(im, _x, _y, x_-_x, y_-_y)
            except:
                print info, im.size, _x, _y, x_, y_
                continue
                #exit()

            hist_img = img.histogram()[255]
            percent = float(hist_img)/float(hist_im)

            img_list.append((img, percent))

        word_side_frame = WordListFrame(img_list)
        word_side_frame.Show()

    def OnGetSide1(self, event):
        img_list = []
        for im, info in self.word_list:
            hist_im = im.histogram()[255]
            if hist_im == 0:
                continue

            _x, _y, x_, y_ = ocr_normalize.GetWordSide1(im)
            #img = im.copy()
            try:
                img = ocr_segmentation.GetWord(im, _x, _y, x_-_x, y_-_y)
            except:
                print info, im.size, _x, _y, x_, y_
                continue
                #exit()

            hist_img = img.histogram()[255]
            percent = float(hist_img)/float(hist_im)

            img_list.append((img, percent))
        print "new"
        word_side_frame = WordListFrame(img_list)
        word_side_frame.Show()

    def OnGetSide2(self, event):
        img_list = []
        for im, info in self.word_list:
            hist_im = im.histogram()[255]
            if hist_im == 0:
                continue

            _x, _y, x_, y_ = ocr_normalize.GetWordSide1(im)
            #img = im.copy()
            try:
                img = ocr_segmentation.GetWord(im, _x, _y, x_-_x, y_-_y)
            except:
                print info, im.size, _x, _y, x_, y_
                continue
                #exit()

            hist_img = img.histogram()[255]
            percent = float(hist_img)/float(hist_im)
            print percent

            if percent < 0.93:
                _nx, _ny, nx_, ny_ = ocr_normalize.ModifyWordSide(im, _x, _y, x_, y_)
                print "_x,_y,x_,y_",_x, _y, x_, y_
                print "new_x,_y,x_,y_",_nx, _ny, nx_, ny_
                print "im size:", im.size
                try:
                    img = ocr_segmentation.GetWord(im, _nx, _ny, nx_-_nx, ny_-_ny)
                except:
                    continue
                hist_img = img.histogram()[255]
                percent = float(hist_img)/float(hist_im)
                if percent < 0.93:
                    print "percent2", percent
                    _x, _y, x_, y_ = _nx, _ny, nx_, ny_
                    _nx, _ny, nx_, ny_ = ocr_normalize.ModifyWordSide(im, _x, _y, x_, y_)
                    try:
                        img = ocr_segmentation.GetWord(im, _nx, _ny, nx_-_nx, ny_-_ny)
                    except:
                        continue
                    hist_img = img.histogram()[255]
                    percent = float(hist_img)/float(hist_im)

            img_list.append((img, percent))
        print "new"
        word_side_frame = WordListFrame(img_list)
        word_side_frame.Show()

    def OnResize(self, event):
        img_list = []
        for im, info in self.word_list:
            img = im.resize((48, 48))
            img_list.append((img, info))

        word_side_frame = WordListFrame(img_list)
        word_side_frame.Show()

    def OnThinning(self, event):
        img_list = []
        for im, info in self.word_list:
            img = thinning.ThinningImage(im)
            img_list.append((img, info))

        word_side_frame = WordListFrame(img_list)
        word_side_frame.Show()


    def OnMatch1(self, event):

        i = 0
        for im, info in self.word_list:
            i += 1
            im.save("test/"+str(i)+".png")
        print "save over!"


