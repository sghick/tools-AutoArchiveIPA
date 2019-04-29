# coding: utf-8

from conf import config
import conf_setting

####################################################################################################
# 处理输入内容
####################################################################################################

sep_line_str = '+----------------------------+'

# 定义输入内容
def receive_input() :
    print('\n' + sep_line_str)
    print('|Branch: ' + config.kBranchName)
    print('|Target: ' + config.kTargetName)
    print(sep_line_str)
    print('|Dev包内网环境请输: 1')
    print('|Dev包外网环境请输: 2')
    print('|AppStore包请输:    3')
    print(sep_line_str)
    print('|打多个包时以空格隔开即可')
    print(sep_line_str)
    print('|可切换至以下项目: ')
    for i in range(len(conf_setting.ConfDocs)) :
        print('|' + conf_setting.ConfDocs[i] + ' e%d' % i)
    print(sep_line_str)
    selectTypes = input('请输入: ')
    print(sep_line_str + '\n')
    return selectTypes

# 解释输入内容,返回packageType, netType
def parser_select_type(selectType) :
    packageType = None
    netType = None
    if selectType == 1:
        packageType = 1
        netType = 1
    elif selectType == 2:
        packageType = 1
        netType = 2
    elif selectType == 3:
        packageType = 2
        netType = 2
    return packageType, netType

# 根据输入类型和配置信息,返回xc打包路径
def parser_xcarchive_path(packageType, netType) :
    xcarchivePath = None
    if packageType == 1:
        if netType == 1:
            xcarchivePath = config.kExportDevInnerPath
        elif netType == 2:
            xcarchivePath = config.kExportDevOuterPath
    elif packageType == 2:
        xcarchivePath = config.kExportAppStorePath
    return xcarchivePath