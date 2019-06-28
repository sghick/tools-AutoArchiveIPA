# coding: utf-8

import os
from utils import alert

####################################################################################################
# smb upload
####################################################################################################

def uploadipa(servicesPathPrefix, validPath, netType, packageType, exprotFileName, folderPath, v) : 
    toValidPath = servicesPathPrefix + validPath
    # 验证安全路径是否存在,如果存在,则创建目标路径,否则判断上传失败
    if not os.path.exists(toValidPath):
        return toValidPath, None, '打包成功（上传SMB失败,未找到服务器路径）！'

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
    return servicesPath, name, alertTitle