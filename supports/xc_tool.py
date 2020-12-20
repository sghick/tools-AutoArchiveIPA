# coding: utf-8

import os
import time
import re
from utils import file_option
from utils import settings
from utils import alert

####################################################################################################
# 处理XCode打包需要做的事
####################################################################################################

# archive并导出ipa
# packageType:  1:Dev包, 2:AppStore包
# netType:      1:内网环境 2:外网环境 3:RC环境
def archive(repositoryName, workspaceName, xcarchivePath, targetName) :
    xcarchiveFilePath = '%s%s.xcarchive' % (xcarchivePath, targetName)
    archiveCommand = "xcodebuild archive -workspace '%s' -scheme '%s' -archivePath '%s'" % (workspaceName, targetName, xcarchiveFilePath)
    print('archiveCommand：' + archiveCommand)
    os.system('%s' % settings.cmd_cd(repositoryName) + ';' + archiveCommand)

    # 检查 archive 是否成功
    if os.path.exists(xcarchiveFilePath) is False:
        alert.show_alert('archive 失败！')
        return False
    return True

# 读入info配置
def readipainfo(exportPath, targetName, appIconName):
    infoplistpath = exportPath + targetName + '.xcarchive/Info.plist'
    icondoc = targetName + '.xcarchive/Products/' + file_option.getApplicationPath(infoplistpath) + '/'
    iconpath = readipaiconinfo(icondoc, appIconName)
    version = file_option.getShortVersion(infoplistpath)
    build = file_option.getVersion(infoplistpath)
    bundleid = file_option.getBundleID(infoplistpath)
    return version, build, bundleid, iconpath

def readipaiconinfo(icondoc, appIconName):
    iconpath = icondoc + appIconName + '60x60@3x.png'
    return iconpath

def exportipa(repositoryName, exportPath, targetName, exportOptionName, packageType, netType, v):
    curTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    folderName = '%s %s' % (targetName, curTime)
    folderPath = '%s%s/%s/' % (exportPath, v, folderName)
    file_option.createFolderIfNeed(folderPath)
    # 找到 .xcarchive 文件
    xcarchiveFileName = targetName + '.xcarchive'
    xcarchiveFilePath = exportPath + xcarchiveFileName
    # ExportOptions-xxx.plist 文件
    exportOptionsFilePath = None
    if packageType == 1:
        exportOptionsFilePath = settings.export_option_dev_path(exportOptionName)
    elif packageType == 2:
        exportOptionsFilePath = settings.export_option_dis_path(exportOptionName)
    if not os.path.exists(exportOptionsFilePath) :
        alert.show_alert('导出 ipa 失败~\n缺少文件 ExportOptions.plist\n请仔细阅读使用说明!')
        return
    # 导出ipa包
    exportArchiveCommand = "xcodebuild -exportArchive -archivePath '%s' -exportPath '%s' -exportOptionsPlist '%s'" % (
    xcarchiveFilePath, folderPath, exportOptionsFilePath)
    print('exportArchiveCommand：' + exportArchiveCommand)
    os.system('%s' % settings.cmd_cd(repositoryName) + ';' + exportArchiveCommand)
    ipaFilePath = folderPath + file_option.getFilePath(folderPath, '.ipa')
    # 检查导出 ipa 是否成功
    if os.path.exists(ipaFilePath) is False:
        alert.show_alert('未到找 ipa 文件！')
        return
    # 把 ipa 包重新命名下
    nn = None
    if netType == 1:
        nn = '内网'
    else:
        nn = '外网'
    pn = None
    if packageType == 1:
        pn = 'Dev'
    else:
        pn = 'Dis'
    exprotFileName = targetName + '-' + v + '-' + nn + '-' + pn
    newIpaFilePath = folderPath + '/' + exprotFileName + '.ipa'
    file_option.fileRename(ipaFilePath, newIpaFilePath)
    # 导出成功后再移动 .xcarchive 文件到新目录中
    newXcarchiveFilePath = folderPath + xcarchiveFileName
    file_option.moveFileToFolder(xcarchiveFilePath, newXcarchiveFilePath)
    return exprotFileName, folderPath

def exportdSYMFile(exprotFileName, folderPath, targetName):
    # .dSYM 文件到新目录中
    dSYMPath = folderPath + targetName + '.xcarchive/dSYMs/' + targetName.lower() + '.app.dSYM'
    dSYMToOutputPath = folderPath + exprotFileName + '.dSYM'
    print('dSYM:' + dSYMPath)
    print('dSYM out put:' + dSYMToOutputPath)
    file_option.copyFolderToFolder(dSYMPath, dSYMToOutputPath)
