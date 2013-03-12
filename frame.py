#coding=utf8

from PIL import Image
import wx
import os
from ImageTool import *
import ocr_binary_image #二值化模块

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "OCR",size=(500,400))
        self.sw = wx.ScrolledWindow(self)
        #设置图标
        icon = wx.Icon('icon.png', wx.BITMAP_TYPE_PNG)
        #icon = wx.EmptyIcon()
        #icon.CopyFromBitmap(wx.BitmapFromImage(wx.Image(("icon.png"), wx.BITMAP_TYPE_PNG)))
        self.SetIcon(icon)

        #文字识别状态

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

        #Edit
        self.menu_ocr = wx.Menu()
        self.menu_OCR=self.menu_ocr.Append(-1,"OCR\n文字识别") #字符识别
        self.menu_ocr.AppendSeparator()
        self.menu_convert=self.menu_ocr.Append(-1,"Convert Image\n图像灰度化")
        self.Bind(wx.EVT_MENU, self.OnConvert, self.menu_convert)

        self.menu_binary=self.menu_ocr.Append(-1,"Binary Image\n图像二值化")
        self.Bind(wx.EVT_MENU, self.OnBinary, self.menu_binary)

        self.menu_denoise = self.menu_ocr.Append(-1, "Image Denoising\n图像去噪")#图像去噪

        self.menu_tilt=self.menu_ocr.Append(-1,"Tilt Correction\n倾斜处理") #倾斜处理

        self.menu_segmentation=self.menu_ocr.Append(-1,"Character Segmentation\n字符切割") #字符切割

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

        menuBar = wx.MenuBar()
        menuBar.Append(self.menu_file, "File")
        menuBar.Append(self.menu_ocr, "OCR")
        menuBar.Append(self.menu_help, "Help")

        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        #显示面板
        self.Canvas = wx.StaticBitmap(self.sw, bitmap=wx.EmptyBitmap(0,0))
        self.image=[] #PIL.Image list 显示第一个
    
    def CanvasUpdate(self):
        ''' 显示图像'''
        if self.image:
            img=pilImage_to_wxImage(self.image[0])
            self.Canvas.SetBitmap(wx.BitmapFromImage(img))
            self.sw.SetScrollbars(1, 1,img.GetWidth(), img.GetHeight())
        else:
            self.Canvas.SetBitmap(wx.EmptyBitmap(1,1))
            self.sw.SetScrollbars(0, 0,0,0)

    def ClearImage(self):
        ''' 清除图像'''
        self.image=[]
        self.CanvasUpdate()

    def OnClear(self,event):
        ''' 清除图片'''
        self.ClearImage()

    def OnConvert(self,event):
        """ 图像灰度化"""
        img=ocr_binary_image.ConvertImage(self.image[0])
        self.image.insert(0,img)
        self.CanvasUpdate()
        self.menu_binary.Enable(True)
        
    def OnBinary(self,event):
        ''' 二值化 '''
        img=ocr_binary_image.BinaryImage(self.image[0])
        self.image.insert(0,img)
        self.CanvasUpdate()

    def OnLoad(self, event):
        ''' 装载'''
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
        self.CanvasUpdate()
        #菜单允许
        self.menu_clear.Enable(True)
        self.menu_OCR.Enable(True)
        self.menu_convert.Enable(True)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawLine(50, 60, 190, 60)

    def OnExit(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
