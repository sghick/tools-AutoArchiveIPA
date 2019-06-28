# coding: utf-8

import os

####################################################################################################
# 基本路径的配置-推荐不要修改
####################################################################################################

# 脚本的存放目录,不需要修改
kScriptRootPath = os.getcwd() + '/'
# 脚本配置的根目录,不需要修改
kAutoArchiveConifgRootPath = kScriptRootPath + 'conf/'
# 源代码存放的根目录,不需要修改
kAutoArchiveRepositoryRootPath = kScriptRootPath + '__repository/'
# 输出文件的根目录,不需要修改
kAutoArchiveExportRootPath = kScriptRootPath + '__export/'

# '.xcodeproj/.xcworkspace/Podfile'文件所在目录,必须将这些文件放在同一个目录下,用于执行build命令和git命令
def cmd_cd(repositoryName):
    return 'cd %s' % kAutoArchiveRepositoryRootPath + repositoryName

def export_option_dis_path(targetName):
    return kAutoArchiveConifgRootPath + targetName + '-Dis-ExportOptions.plist'
def export_option_dev_path(targetName):
    return kAutoArchiveConifgRootPath + targetName + '-Dev-ExportOptions.plist'

def export_path_app_store(repositoryName):
    return kAutoArchiveExportRootPath + repositoryName + 'AppStore/'

def export_path_dev_inner(repositoryName):
    return kAutoArchiveExportRootPath + repositoryName + 'DevInner/'

def export_path_dev_outer(repositoryName):
    return kAutoArchiveExportRootPath + repositoryName + 'DevOuter/'

