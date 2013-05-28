#-*- encoding:UTF-8 -*-
import wx
import ImageTool


class WordListFrame(wx.Frame):
    def __init__(self, word_list):
        wx.Frame.__init__(self, None, -1,
                          "PyOCR",
                          size=(600, 400))

        # load some images into an image list
        #创建图像列表
        w, h = word_list[0][0].size
        il = wx.ImageList(w, h, True)
        for im, _x, _y in word_list:
            #im.save(str(_x)+str(_y)+".png")
            img = ImageTool.pilImage_to_wxImage(im)
            bmp = wx.BitmapFromImage(img)
            il_max = il.Add(bmp)

        # create the list control
        #创建列表窗口部件
        self.list = wx.ListCtrl(self, -1,
                style=wx.LC_ICON | wx.LC_AUTOARRANGE)

        # assign the image list to it
        self.list.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

        # create some items for the list
        #为列表创建一些项目
        for x in range(25):
            img = x % (il_max+1)
            self.list.InsertImageStringItem(x,
                    "%02d" % x, img)

