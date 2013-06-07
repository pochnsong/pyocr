#coding=utf8
"""
2013 ПМ-ПУ
Сун Цзыжу
BOOTING

"""
from PIL import Image
import wx
from wx import xrc

import os
from ImageTool import *
#二值化模块
import ocr_binary_image
#去噪
import ocr_denoice_image
 #字符切割
import ocr_segmentation
import ImageEditor
import frame_xrc
import word_list_frame

APPICON = "icon.png"


class MyFrame(frame_xrc.xrcMain):
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.

        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle()."""
        pass

    def __init__(self):
        frame_xrc.xrcMain.__init__(self, None)
        #设置图标
        icon = wx.Icon(APPICON, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        #File
        self.Bind(wx.EVT_MENU, self.OnLoad, id=xrc.XRCID("menu_load"))
        self.Bind(wx.EVT_MENU, self.OnClear, id=xrc.XRCID("menu_clear"))
        self.Bind(wx.EVT_MENU, self.OnExit, id=xrc.XRCID("menu_exit"))

        #OCR
        self.Bind(wx.EVT_MENU, self.OnConvert, id=xrc.XRCID("menu_convert"))
        self.Bind(wx.EVT_MENU, self.OnBinary, id=xrc.XRCID("menu_binary"))
        self.Bind(wx.EVT_MENU, self.OnMedianFilter, id=xrc.XRCID("menu_median_filter"))
        self.Bind(wx.EVT_MENU, self.OnSegmentation, id=xrc.XRCID("menu_segmentation"))
        self.Bind(wx.EVT_MENU, self.OnFCMNormal, id=xrc.XRCID("menu_fcm_normal"))
        self.Bind(wx.EVT_MENU, self.OnFCMFast, id=xrc.XRCID("menu_fcm_fast"))
        self.Bind(wx.EVT_MENU, self.OnFCMBlock, id=xrc.XRCID("menu_fcm_block"))
        self.Bind(wx.EVT_MENU, self.OnKMeans, id=xrc.XRCID("menu_kmeans"))
        self.Bind(wx.EVT_MENU, self.OnWordShow, id=xrc.XRCID("menu_word_show"))
        self.Bind(wx.EVT_MENU, self.OnKMeansFast, id=xrc.XRCID("menu_kmeans_fast"))
        self.Bind(wx.EVT_MENU, self.OnBorder, id=xrc.XRCID("menu_border"))

        #debug
        self.Bind(wx.EVT_MENU, self.OnDebug_undo, id=xrc.XRCID("menu_undo"))
        self.Bind(wx.EVT_MENU, self.OnDebug_hist, id=xrc.XRCID("menu_gray_hist"))
        self.Bind(wx.EVT_MENU, self.OnDebug_dist, id=xrc.XRCID("menu_dist"))

        #Edit
        self.Bind(wx.EVT_MENU, self.OnZoomIn, id=xrc.XRCID("menu_zoom_in"))
        self.Bind(wx.EVT_MENU, self.OnZoomOut, id=xrc.XRCID("menu_zoom_out"))

        #显示面板
        self.sw = xrc.XRCCTRL(self, "sw")
        self.Canvas = xrc.XRCCTRL(self, "Canvas")
        self.statusbar = self.GetStatusBar()
        self.image=[] #PIL.Image list 显示第一个
        #文字识别状态
        self.status=[""] #状态使用最后一个
        self.zoom=100 #缩放级别
        self.MenuUpdate()

    def MenuUpdate(self):
        """ 菜单更新
        菜单允许规则
        """
        #File
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_clear")).Enable("src" in self.status)

        #OCR
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_OCR")).Enable("src" in self.status) #字符识别
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_convert")).Enable("src" in self.status)
        #self.menu_median_filter.Enable("src" in self.status)
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_binary")).Enable("convert" in self.status)
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_median_filter")).Enable("src" in self.status)#图像去噪 медианный фильтр median filter dct
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_tilt")).Enable(False) #倾斜处理
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_segmentation")).Enable("binary" in self.status)#字符切割
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_recognition")).Enable("segmentation" in self.status)#字符识别
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_proofread")).Enable(False) #结果校对
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_fcm_normal")).Enable("src" in self.status)
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_kmeans")).Enable("binary" in self.status)

        #debug
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_undo")).Enable(len(self.status)>1)
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_gray_hist")).Enable("convert" in self.status)
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_dist")).Enable("binary" in self.status) #

        #edit
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_zoom_in")).Enable("src" in self.status) #放大
        self.GetMenuBar().FindItemById(xrc.XRCID("menu_zoom_out")).Enable("src" in self.status) #缩小

    #---------------------------------------------------------------
    def OnZoomIn(self, event):
        self.zoom+=20
        self.CanvasUpdate()
        self.StatusBarUpdate()

    def OnZoomOut(self,event):
        self.zoom-=20
        if self.zoom<2:
            self.zoom=2

        self.CanvasUpdate()
        self.StatusBarUpdate()


    def OnDebug_undo(self,event):
        """
        Undo
        """
        self.image.pop(0)
        self.status.pop()
        self.CanvasUpdate()

    def OnDebug_dist(self,event):
        """
        背景分布
        """
        class HistFrame(wx.Frame):
            def __init__(self,image,direction):
                """ image=PIL.Image"""
                dist=ocr_segmentation.BackgroundDistList(image,direction)
                img=ocr_segmentation.DistImage(dist,direction)
                wx.Frame.__init__(self, None, -1, "BG "+direction,size=img.size)
                icon = wx.Icon(APPICON, wx.BITMAP_TYPE_PNG)
                self.SetIcon(icon)
                sw = wx.ScrolledWindow(self)
                img=pilImage_to_wxImage(img)
                wx.StaticBitmap(sw, bitmap=wx.BitmapFromImage(img))
                sw.SetScrollbars(1, 1,img.GetWidth(), img.GetHeight())

                pass
            pass

        dialog_debug=HistFrame(self.image[0],'h')
        dialog_debug.Show()
        dialog_debug=HistFrame(self.image[0],'w')
        dialog_debug.Show()

    def OnDebug_hist(self,event):
        """Debug
        灰度直方图"""
        class HistFrame(wx.Frame):
            def __init__(self,image):
                """ image=PIL.Image"""
                wx.Frame.__init__(self, None, -1, "Histogram",size=(256,200))
                icon = wx.Icon(APPICON, wx.BITMAP_TYPE_PNG)
                self.SetIcon(icon)

                img=ocr_binary_image.HistogramImage(image,256,200)
                img=pilImage_to_wxImage(img)
                Canvas = wx.StaticBitmap(self, bitmap=wx.BitmapFromImage(img))
                pass
            pass
        dialog_debug=HistFrame(self.image[0])
        dialog_debug.Show()

    def CanvasUpdate(self):
        """ 显示图像"""
        if self.image:
            #图像视觉缩放
            image=self.image[0]
            if self.zoom !=100:
                image=ImageEditor.Zoom(image,float(self.zoom)/100.0)

            img=pilImage_to_wxImage(image)
            self.Canvas.SetBitmap(wx.BitmapFromImage(img))
            self.sw.SetScrollbars(1, 1,img.GetWidth(), img.GetHeight())
        else:
            self.Canvas.SetBitmap(wx.EmptyBitmap(1,1))
            self.sw.SetScrollbars(0, 0,0,0)

        self.MenuUpdate()

    def StatusBarUpdate(self):
        """ 更新状态栏"""
        if self.image:
            w,h=self.image[0].size
            self.statusbar.SetStatusText(str(w)+'*'+str(h),0)
            self.statusbar.SetStatusText(str(self.zoom)+"%",1)
        else:
            self.statusbar.SetStatusText("",0)
            self.statusbar.SetStatusText("",1)

    def ClearImage(self):
        """ 清除图像"""
        self.zoom=100
        self.image=[]
        self.status=[""]
        self.CanvasUpdate()

    def OnClear(self,event):
        """ 清除图片"""
        self.ClearImage()
        self.StatusBarUpdate()

    def OnConvert(self,event):
        """ 图像灰度化"""
        img=ocr_binary_image.ConvertImage(self.image[0])

        self.image.insert(0,img)
        self.status.append("convert")
        self.CanvasUpdate()

    def OnMedianFilter(self,event):
        """ 中值滤波"""
        dlg = wx.TextEntryDialog(None, "size of median filter",
                                 'Median Filter', '3')
        size=None
        if dlg.ShowModal() == wx.ID_OK:
            size = int(dlg.GetValue())
        dlg.Destroy()

        if size:
            img = ocr_denoice_image.MedianFilter(self.image[0],size)
            self.image.insert(0,img)
            self.status.append("median_filter")
            self.CanvasUpdate()

    def OnFCMNormal(self,event):
        img = ocr_denoice_image.Denoice_FCM_Normal(self.image[0])
        self.image.insert(0,img)
        self.status.append("denoise")
        self.CanvasUpdate()

    def OnFCMFast(self, event):
        img = ocr_denoice_image.Denoice_FCM_Fast(self.image[0])

        self.image.insert(0, img)
        self.status.append("binary")
        self.CanvasUpdate()

    def OnFCMBlock(self, event):

        img = ocr_denoice_image.Denoice_FCM_block(self.image[0])
        self.image.insert(0, img)
        self.status.append("denoise")
        self.CanvasUpdate()

    def OnKMeans(self, event):
        img = ocr_denoice_image.Denoise_kmeans(self.image[0])
        self.image.insert(0, img)
        self.status.append("denoise")
        self.CanvasUpdate()

    def OnKMeansFast(self, event):
        img = ocr_denoice_image.Denoise_kmeans_fast(self.image[0])
        self.image.insert(0, img)
        self.status.append("denoise")
        self.CanvasUpdate()

    def OnBinary(self, event):
        """ 二值化 """
        img = ocr_binary_image.BinaryImage(self.image[0])

        self.image.insert(0, img)
        self.status.append("binary")
        self.CanvasUpdate()

    def OnSegmentation(self, event):
        """
        字符切割
        """
        img, self.im_list = ocr_segmentation.Segmentation(self.image[0])
        self.image.insert(0, img)
        self.status.append("segmentation")
        self.CanvasUpdate()

    def OnWordShow(self, event):
        """
        字符切割
        """
        word_show = word_list_frame.WordListFrame(self.im_list)
        word_show.Show()

    def OnBorder(self, event):
        """
        处理边界处留白
        """
        img = ocr_denoice_image.RemoveBlankBorder(self.image[0])
        self.image.insert(0, img)
        self.status.append("remove border")
        self.CanvasUpdate()

        pass

    def OnLoad(self, event):
        """ 装载"""
        load_dialog=wx.FileDialog(None,"Choose a Image",os.getcwd(),
                                  "","All (*.*)|*.*",wx.OPEN)

        fname=""
        if load_dialog.ShowModal()==wx.ID_OK:
            fname=load_dialog.GetPath()
        else:
            load_dialog.Destroy()
            return

        img=Image.open(fname)
        self.image=[img]
        self.status=["src"]
        self.CanvasUpdate()
        #状态栏
        self.StatusBarUpdate()

    def OnExit(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
