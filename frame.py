#coding=utf8
"""
2013 ПМ-ПУ
Сун Цзыжуй
"""
from PIL import Image
import wx
import os
from ImageTool import *
import ocr_binary_image #二值化模块
import ocr_denoice_image #去噪
import ocr_segmentation #字符切割
import ImageEditor

APPICON="icon.png"

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "OCR",size=(400,500))
        self.sw = wx.ScrolledWindow(self)
        #设置图标
        icon = wx.Icon(APPICON, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        #File
        self.menu_file = wx.Menu()
        self.menu_load = self.menu_file.Append(-1, "Load Image\n装载图像") #装载碑文图片
        self.Bind(wx.EVT_MENU, self.OnLoad, self.menu_load)

        self.menu_clear = self.menu_file.Append(-1, "Clear Image\n清除图像") #清除碑文图片
        self.menu_clear.Enable(False)
        self.Bind(wx.EVT_MENU, self.OnClear, self.menu_clear)

        self.menu_file.AppendSeparator()
        self.menu_exit = self.menu_file.Append(-1, "Exit\n退出")
        self.Bind(wx.EVT_MENU, self.OnExit, self.menu_exit)

        #OCR
        self.menu_ocr = wx.Menu()
        self.menu_OCR=self.menu_ocr.Append(-1,"OCR\n文字识别") #字符识别
        self.menu_ocr.AppendSeparator()
        self.menu_convert=self.menu_ocr.Append(-1,"Convert Image\n图像灰度化")
        self.Bind(wx.EVT_MENU, self.OnConvert, self.menu_convert)


        self.menu_binary=self.menu_ocr.Append(-1,"Binary Image\n图像二值化")
        self.Bind(wx.EVT_MENU, self.OnBinary, self.menu_binary)

        submenu_dinoise=wx.Menu()
        median_filter=submenu_dinoise.Append(-1,"Median Filter\n中值滤波")#图像去噪 медианный фильтр median filter dct
        self.Bind(wx.EVT_MENU, self.OnMedianFilter,median_filter)
        self.menu_denoise = self.menu_ocr.AppendMenu(-1, "Image Denoising\n图像去噪",submenu_dinoise)#图像去噪

        self.menu_tilt=self.menu_ocr.Append(-1,"Tilt Correction\n倾斜处理") #倾斜处理

        self.menu_segmentation=self.menu_ocr.Append(-1,"Character Segmentation\n字符切割") #字符切割
        self.Bind(wx.EVT_MENU, self.OnSegmentation, self.menu_segmentation)

        self.menu_recognition=self.menu_ocr.Append(-1,"Character Recognition\n文字识别") #字符识别
        self.menu_proofread=self.menu_ocr.Append(-1,"Proofread\n结果校对") #结果校对

        #菜单状态
        for i in self.menu_ocr.GetMenuItems():
            i.Enable(False)

        #Help
        self.menu_help = wx.Menu()
        self.menu_doc=self.menu_help.Append(-1,"Documentation\n文档") #文档
        self.menu_help.AppendSeparator()
        self.menu_about=self.menu_help.Append(-1,"About\n关于") #关于

        #debug
        self.menu_debug = wx.Menu()
        self.menu_undo=self.menu_debug.Append(-1,"Undo")
        self.Bind(wx.EVT_MENU, self.OnDebug_undo, self.menu_undo)
        self.menu_hist=self.menu_debug.Append(-1,"Gary Histogram") #
        self.Bind(wx.EVT_MENU, self.OnDebug_hist, self.menu_hist)
        self.menu_dist=self.menu_debug.Append(-1,"Distribution") #
        self.Bind(wx.EVT_MENU, self.OnDebug_dist, self.menu_dist)

        #Edit
        self.menu_edit=wx.Menu()
        self.menu_zoom_in=self.menu_edit.Append(-1,"Zoom In") #放大
        self.Bind(wx.EVT_MENU, self.OnZoomIn, self.menu_zoom_in)
        self.menu_zoom_out=self.menu_edit.Append(-1,"Zoom Out") #缩小
        self.Bind(wx.EVT_MENU, self.OnZoomOut, self.menu_zoom_out)

        menuBar = wx.MenuBar()
        menuBar.Append(self.menu_file, "File")
        menuBar.Append(self.menu_edit,"Edit")
        menuBar.Append(self.menu_debug, "Debug")
        menuBar.Append(self.menu_ocr, "OCR")
        menuBar.Append(self.menu_help, "Help")

        self.SetMenuBar(menuBar)
        self.statusbar=self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)

        #显示面板
        self.Canvas = wx.StaticBitmap(self.sw, bitmap=wx.EmptyBitmap(0,0))
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
        self.menu_load.Enable(True) #装载碑文图片
        self.menu_clear.Enable("src" in self.status)
        self.menu_exit.Enable(True)

        #OCR
        self.menu_OCR.Enable("src" in self.status) #字符识别
        self.menu_convert.Enable("src" in self.status)
        #self.menu_median_filter.Enable("src" in self.status)
        self.menu_binary.Enable("convert" in self.status)
        self.menu_denoise.Enable("src" in self.status)#图像去噪 медианный фильтр median filter dct
        self.menu_tilt.Enable(False) #倾斜处理
        self.menu_segmentation.Enable("binary" in self.status)#字符切割
        self.menu_recognition.Enable("segmentation" in self.status)#字符识别
        self.menu_proofread.Enable(False) #结果校对

        #Help
        self.menu_doc.Enable(True)#文档
        self.menu_about.Enable(True) #关于

        #debug
        self.menu_undo.Enable(len(self.status)>1)
        self.menu_hist.Enable("convert" in self.status)
        self.menu_dist.Enable("binary" in self.status) #

        #edit
        self.menu_zoom_in.Enable("src" in self.status) #放大
        self.menu_zoom_out.Enable("src" in self.status) #缩小

    #---------------------------------------------------------------
    def OnZoomIn(self,event):
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
            img=ocr_denoice_image.MedianFilter(self.image[0],size)
            self.image.insert(0,img)
            self.status.append("median_filter")
            self.CanvasUpdate()

    def OnBinary(self,event):
        """ 二值化 """
        img=ocr_binary_image.BinaryImage(self.image[0])
        self.image.insert(0,img)
        self.status.append("binary")
        self.CanvasUpdate()

    def OnSegmentation(self,event):
        """
        字符切割
        """
        img=ocr_segmentation.Segmentation(self.image[0])
        self.image.insert(0,img)
        self.status.append("segmentation")
        self.CanvasUpdate()

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
