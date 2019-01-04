# coding: utf-8

import os
from conf import config

####################################################################################################
# 文件操作的定义
####################################################################################################

# 根据传入的文件路径，获取这个文件的文本内容
def read_file(fpath) :
    f = None
    # 文件内容
    text = None
    fileReadErrorReason = None
    try:
        # 打开文件
        f = open(fpath, 'r')
        # 读取文件
        text = f.read()
    except Exception as e:
        fileError = True
        fileReadErrorReason = '读取[' + fpath + ']文件出错！'
        print(fileReadErrorReason)
        print(e)
    finally:
         # 关闭文件
        if f:
            f.close()
        return text, fileReadErrorReason

# 根据传入的文件路径,替换写入text内容
def write_file(fpath, text) :
    fileWriteErrorReason = None
    try:
        # 打开文件
        f = open(fpath, 'w')
        # 写入文件
        f.write(text)
    except Exception as e:
        fileWriteErrorReason = '写入[' + fpath + ']文件出错！'
        print(fileWriteErrorReason)
        print(e)
    finally:
        # 关闭文件
        if f:
            f.close()
    return fileWriteErrorReason


####################################################################################################
# 文件&文件夹操作
####################################################################################################

def copyFileToFolder(filePath, folderPath):
    cmd = "cp '%s' '%s'" % (filePath, folderPath)
    os.system(cmd)

def copyFolderToFolder(folderPath1, folderPath2):
    cmd = "cp -R '%s' '%s'" % (folderPath1, folderPath2)
    os.system(cmd)

def moveFileToFolder(filePath, folderPath):
    cmd = "mv '%s' '%s'" % (filePath, folderPath)
    os.system(cmd)

def fileRename(oldFilePath, newFilePath):
    cmd = "mv '%s' '%s'" % (oldFilePath, newFilePath)
    os.system(cmd)

def createFolderIfNeed(folderPath):
    cmd = "mkdir -p '%s'" % folderPath
    os.system(cmd)

####################################################################################################
# 从 info.plist 获取版本号
####################################################################################################

def getVersionWithKey(key, fpath):
    f = None
    # 文件内容
    text = None
    try:
        # 打开文件
        f = open(fpath, 'r')
        # 读取文件
        text = f.read()
        l = text.split('\n')
        v = None
        flage = False
        for line in l:
            if flage:
                lstripline = line.lstrip()
                start = len('<string>')
                end = len('</string>')
                v = lstripline[start:-end]
                break
            else:
                if key in line:
                    flage = True
        return v
    except Exception as e:
        print('读取 %s 文件出错！', config.kInfoPlistPath)
        print(e)
    finally:
        # 关闭文件
        if f:
            f.close()

def getShortVersion(fpath):
    return getVersionWithKey('CFBundleShortVersionString', fpath)

def getVersion(fpath):
    return getVersionWithKey('CFBundleVersion', fpath)