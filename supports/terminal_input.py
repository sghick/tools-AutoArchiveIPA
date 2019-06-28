# coding: utf-8

from utils import settings

####################################################################################################
# 处理输入内容
####################################################################################################

sep_line_str = '+----------------------------+'

# 定义输入内容
def receive_input(branch, target, confDocs) :
    print('\n' + sep_line_str)
    print('|Branch: ' + branch)
    print('|Target: ' + target)
    print(sep_line_str)
    print('|' + parser_net_name(1) + '请输: 1')
    print('|' + parser_net_name(2) + '请输: 2')
    print('|' + parser_net_name(3) + '请输: 3')
    print(sep_line_str)
    print('|打多个包时以空格隔开即可')
    print('|如需自动上传至fir,请在每个数字后加 -a')
    print(sep_line_str)
    print('|可切换至以下项目: ')
    for i in range(len(confDocs)) :
        print('|' + confDocs[i] + ' e%d' % i)
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
def parser_xcarchive_path(repositoryName, packageType, netType) :
    xcarchivePath = None
    if packageType == 1:
        if netType == 1:
            xcarchivePath = settings.export_path_dev_inner(repositoryName)
        elif netType == 2:
            xcarchivePath = settings.export_path_dev_outer(repositoryName)
    elif packageType == 2:
        xcarchivePath = settings.export_path_app_store(repositoryName)
    return xcarchivePath

def parser_net_name(selectType):
    netname = ''
    if selectType == 1:
        netname = 'Dev包内网环境'
    elif selectType == 2:
        netname = 'Dev包外网环境'
    elif selectType == 3:
        netname = 'AppStore包'
    return netname