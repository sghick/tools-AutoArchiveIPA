# coding: utf-8

import sys
import os
import tkinter
import threading
import time

####################################################################################################
# 弹窗
####################################################################################################

def show_alert(title, autoclose=False):
    alertWindow = tkinter.Tk()
    alertWindow.wm_attributes('-topmost', 1)
    screenWeight, screenHeight = alertWindow.maxsize()
    alertWindow.geometry("240x100+%d+%d" % ((screenWeight - 200) / 2, (screenHeight - 100) / 2))
    alertWindow.resizable(False, False)
    titleLabel = tkinter.Label(alertWindow, text=title, height=3)
    titleLabel.pack()

    def okButtonAction():
        alertWindow.quit()
    if autoclose:
        def auto_close():
            time.sleep(3)
            okButtonAction()
        threading.Thread(target=auto_close).start()
    okButton = tkinter.Button(alertWindow, text='确定', command=okButtonAction, height=1)
    okButton.pack()

    alertWindow.mainloop()

def show_detail_alert(title, archiveFolder, servicesFolder, autoclose=False):
    alertWindow = tkinter.Tk()
    alertWindow.wm_attributes('-topmost', 1)
    screenWeight, screenHeight = alertWindow.maxsize()
    column0Width = 120
    column1Width = 400
    column2Width = 80
    contentWidth = column0Width + column1Width + column2Width
    titleHeight = 44
    pathHeight = 30
    okButtonHeight = 50
    contentHeight = titleHeight + pathHeight*2 + okButtonHeight
    alertWindow.geometry("%sx%s+%d+%d" % (contentWidth, 10 + contentHeight, (screenWeight - 200) / 2, (screenHeight - 100) / 2))
    alertWindow.resizable(False, False)


    titleFrame = tkinter.Frame(width=contentWidth, height=titleHeight)
    titleFrame.grid(row=0, column=0, columnspan=3)

    archiveFolderDescFrame = tkinter.Frame(width=column0Width, height=pathHeight)
    archiveFolderDescFrame.grid(row=1, column=0)
    archiveFolderFrame = tkinter.Frame(width=column1Width, height=pathHeight)
    archiveFolderFrame.grid(row=1, column=1)
    openArchiveFolderButtonFrame = tkinter.Frame(width=column2Width, height=pathHeight)
    openArchiveFolderButtonFrame.grid(row=1, column=2)

    servicesFolderDescLabelFrame = tkinter.Frame(width=column0Width, height=pathHeight)
    servicesFolderDescLabelFrame.grid(row=2, column=0)
    servicesFolderFrame = tkinter.Frame(width=column1Width, height=pathHeight)
    servicesFolderFrame.grid(row=2, column=1)
    openServicesFolderButtonFrame = tkinter.Frame(width=column2Width, height=pathHeight)
    openServicesFolderButtonFrame.grid(row=2, column=2)

    okButtonFrame = tkinter.Frame(width=column2Width, height=okButtonHeight)
    okButtonFrame.grid(row=3, column=0, columnspan=3)


    titleLabel = tkinter.Label(alertWindow, text=title, height=3)
    titleLabel.grid(row=0, column=0, columnspan=3)

    archiveFolderDescLabel = tkinter.Label(alertWindow, text='本地ipa包位置：')
    archiveFolderDescLabel.grid(row=1, column=0, sticky=tkinter.E)
    archiveFolderValue = tkinter.StringVar()
    archiveFolderValue.set(archiveFolder)
    archiveFolderEntry = tkinter.Entry(alertWindow, textvariable=archiveFolderValue)
    archiveFolderEntry.grid(row=1, column=1, sticky=tkinter.EW)
    def openArchiveFolderButtonAction():
        os.system("open '%s'" % archiveFolderEntry.get())
    openArchiveFolderButton = tkinter.Button(alertWindow, text='打开', command=openArchiveFolderButtonAction)
    openArchiveFolderButton.grid(row=1, column=2)

    servicesFolderDescLabel = tkinter.Label(alertWindow, text='服务器ipa包位置：')
    servicesFolderDescLabel.grid(row=2, column=0, sticky=tkinter.E)
    servicesFolderValue = tkinter.StringVar()
    servicesFolderValue.set(servicesFolder)
    servicesFolderEntry = tkinter.Entry(alertWindow, textvariable=servicesFolderValue)
    servicesFolderEntry.grid(row=2, column=1, sticky=tkinter.EW)
    def openServicesFolderButtonAction():
        os.system("open '%s'" % servicesFolderEntry.get())
    openServicesFolderButton = tkinter.Button(alertWindow, text='打开', command=openServicesFolderButtonAction)
    openServicesFolderButton.grid(row=2, column=2)

    def okButtonAction():
        alertWindow.quit()
    if autoclose:
        def auto_close():
            time.sleep(3)
            okButtonAction()
        threading.Thread(target=auto_close).start()
    okButton = tkinter.Button(alertWindow, text='确定', command=okButtonAction)
    okButton.grid(row=3, column=0, columnspan=3)

    alertWindow.mainloop()

if __name__ == '__main__':
    # show_alert('测试自动关闭', autoclose=True)
    # show_alert('拷贝 dSYM 文件到服务器失败！', autoclose=False)
    # show_detail_alert(title='打包成功！', archiveFolder='/Users/us/Desktop/', servicesFolder='smb://10.11.102.111/xxxx/测试/测试安装包')
    title = ''
    archiveFolder = ''
    servicesFolder = ''
    if len(sys.argv) >= 1:
        title = sys.argv[1]
    if len(sys.argv) >= 2:
        archiveFolder = sys.argv[2]
    if len(sys.argv) >= 3:
        servicesFolder = sys.argv[3]
    show_detail_alert(title, archiveFolder, servicesFolder, True)
