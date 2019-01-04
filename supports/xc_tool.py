# coding: utf-8

import os
import time
from supports import alert
from supports import file_option
from conf import config

####################################################################################################
# 处理XCode打包需要做的事
####################################################################################################

# archive并导出ipa
# packageType:  1:Dev包, 2:AppStore包
# netType:      1:内网环境 2:外网环境
def archive(workspaceName, xcarchivePath, targetName) :
    xcarchiveFilePath = '%s%s.xcarchive' % (xcarchivePath, targetName)
    archiveCommand = "xcodebuild archive -workspace '%s' -scheme '%s' -archivePath '%s'" % (workspaceName, targetName, xcarchiveFilePath)
    print('archiveCommand：' + archiveCommand)
    os.system('%s' % config.cdCommand + ';' + archiveCommand)

    # 检查 archive 是否成功
    if os.path.exists(xcarchiveFilePath) is False:
        alert.show_alert('archive 失败！')
        return False
    return True

def exportipa(exportPath, targetName, packageType, netType):
    curTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    infoplistpath = exportPath + targetName + '.xcarchive' + '/' + 'Info.plist'
    v = file_option.getVersion(infoplistpath)
    folderName = '%s %s' % (targetName, curTime)
    folderPath = '%s%s/%s/' % (exportPath, v, folderName)
    file_option.createFolderIfNeed(folderPath)
    # 找到 .xcarchive 文件
    xcarchiveFileName = targetName + '.xcarchive'
    xcarchiveFilePath = exportPath + xcarchiveFileName
    # ExportOptions-xxx.plist 文件
    exportOptionsFilePath = None
    if packageType == 1:
        exportOptionsFilePath = config.kExportOptionsDevPath
    elif packageType == 2:
        exportOptionsFilePath = config.kExportOptionsAppStorePath
    if not os.path.exists(exportOptionsFilePath) :
        alert.show_alert('导出 ipa 失败~\n缺少文件 ExportOptions.plist\n请仔细阅读使用说明!')
        return
    # 导出ipa包
    exportArchiveCommand = "xcodebuild -exportArchive -archivePath '%s' -exportPath '%s' -exportOptionsPlist '%s'" % (
    xcarchiveFilePath, folderPath, exportOptionsFilePath)
    print('exportArchiveCommand：' + exportArchiveCommand)
    os.system('%s' % config.cdCommand + ';' + exportArchiveCommand)
    ipaFilePath = folderPath + targetName + '.ipa'
    # 检查导出 ipa 是否成功
    if os.path.exists(ipaFilePath) is False:
        alert.show_alert('导出 ipa 失败！')
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

def uploadService(netType, packageType, exprotFileName, folderPath) : 
    toValidPath = config.kServicesPathPrefix + config.kValidPath
    # 验证安全路径是否存在,如果存在,则创建目标路径,否则判断上传失败
    if not os.path.exists(toValidPath):
        return toValidPath, None, '打包成功（上传失败,未找到服务器路径）！'

    isAppStore = False
    nn = None
    if netType == 1:
        nn = '内网'
    else:
        nn = '外网'

    if netType == 2 and packageType == 2:
        isAppStore = True
    if isAppStore:
        sfn = 'AppStore'
    else:
        sfn = nn
    # 版本号,从dSYM文件中获取
    dSYMFilePath = folderPath + exprotFileName + '.dSYM'
    infoplistpath = dSYMFilePath + '/Contents/Info.plist'
    v = file_option.getVersion(infoplistpath)
    # 生成服务器存放ipa包的路径
    servicesPath = toValidPath + v[0:len(v) - len(v.split('.')[-1]) - 1] + '/' + sfn + '/'
    ipaIdx = 1
    if os.path.exists(servicesPath):
        # 遍历文件夹中的文件寻找到ipa包的最大的下标
        has = False
        for n in os.listdir(servicesPath):
            if n.endswith('.ipa'):
                idxStr = n[0:len(n) - len('.ipa')].split('-')[-1]
                if idxStr.isdigit():
                    has = True
                    idx = int(idxStr)
                    if idx > ipaIdx:
                        ipaIdx = idx
        if has:
            ipaIdx += 1
    else:
        # 创建文件夹
        file_option.createFolderIfNeed(servicesPath)

    name = exprotFileName + '-' + str(ipaIdx)
    # 根据ipaIdx重命名ipa包
    ipaPath = folderPath + exprotFileName + '.ipa'
    newIpaPath = folderPath + name + '.ipa'
    file_option.fileRename(ipaPath, newIpaPath)
    ipaPath = newIpaPath
    ipaToServicesPath = servicesPath + name + '.ipa'
    if config.kCopyIpaToServices:
        # 拷贝ipa包到服务器
        file_option.copyFileToFolder(ipaPath, ipaToServicesPath)

        copyIpaError = False
        # 检查拷贝 ipa 包到服务器是否成功
        if os.path.exists(ipaToServicesPath) is False:
            # 拷贝 ipa 包到服务器失败！
            copyIpaError = True

        copydSYMError = False
        if isAppStore:
            # 拷贝 dSYM 文件到服务器
            dSYMToServicesPath = servicesPath + name + '.dSYM'
            file_option.copyFolderToFolder(dSYMFilePath, dSYMToServicesPath)
            print('uploadService-dSYMFilePath:' + dSYMFilePath)
            print('uploadService-dSYMToServicesPath:' + dSYMToServicesPath)
            # 检查拷贝 dSYM 文件到服务器是否成功
            if os.path.exists(dSYMToServicesPath) is False:
                # 拷贝 dSYM 文件到服务器失败！
                copydSYMError = True
        alertTitle = ''
        if copyIpaError is False and copydSYMError is False:
            alertTitle = '打包成功（已拷贝到服务器）！' + '[' + name + ']'
        elif copyIpaError is True or copydSYMError is True:
            alertTitle = '打包成功（拷贝到服务器失败）！' + '[' + name + ']'
        else:
            if copyIpaError is True:
                alertTitle = '打包成功（ipa 拷贝到服务器失败）！' + '[' + name + ']'
            elif copydSYMError is True:
                alertTitle = '打包成功（dSYM 拷贝到服务器失败）！' + '[' + name + ']'
            else:
                pass # 不处理
    else:
        alertTitle = '打包成功（未拷贝到服务器）！' + '[' + name + ']'
    return servicesPath, name, alertTitle