# coding: utf-8

from utils import file_option
from utils import alert
from utils import settings

sep_line_str = '+----------------------------+'

####################################################################################################
# 更改打包配置
####################################################################################################

def safe_change_conf_python3(inputs, confDocs) :
    fmt = inputs[0][:2]
    idx = inputs[0][2:]

    if (fmt == '-e') :
        try:
            if len(idx)==0 :
                print("参数错误!")
                return False
            if change_conf_python3(idx, len(confDocs)):
                print("成功切换至: " + confDocs[int(idx)])
                restarCmd = "python3 %s" % settings.kScriptRootPath + 'archive.py'
                print('请重启脚本: ' + restarCmd)
            else:
                print('切换配置失败.')
        except:
            print("未找到相关配置!")
        return False
    return True

def change_conf_python3(idx, lenconfig):
    if int(idx) >= lenconfig:
        return
    fpath = settings.kAutoArchiveConifgRootPath + 'config.py'
    markcode = 'CurrentConfigIndex = '
    # 获取代码配置文件内容
    text, fileReadErrorReason = file_option.read_file(fpath)
    # 检查操作代码配置文件是否失败
    if text is None:
        alert.show_alert(fileReadErrorReason)
        return False
    codeline = ''
    tl = text.split('\n')
    for line in tl:
        if line[:len(markcode)]==markcode:
            codeline = line
            break
    if not codeline:
        return
    text = text.replace(codeline, markcode + idx)

    # 写入代码配置文件内容
    fileWriteErrorReason = file_option.write_file(fpath, text)
    # 检查操作失败,弹窗提示
    if fileWriteErrorReason is not None :
        alert.show_alert(fileWriteErrorReason)
        return False
    else :
        return True


####################################################################################################
# 更改代码配置
####################################################################################################

def safe_change_code_config_network(netType, configFilePath, netStatusForDevCode, netStatusForDisCode, netStatusForRCCode) :
    filePath = None
    try:
        filePath = settings.kAutoArchiveRepositoryRootPath + configFilePath
        print(filePath)
    except:
        print("未定义代码配置文件!")

    if filePath:
        change_code_config_network(netType, filePath, netStatusForDevCode, netStatusForDisCode, netStatusForRCCode)

# 切换代码中配置文件的网络环境配置
# netType:  1:内网,2:外网,3:ADHoc
# fpath:    代码的配置文件路径
def change_code_config_network(netType, fpath, netStatusForDevCode, netStatusForDisCode, netStatusForRCCode) :
    # 获取代码配置文件内容
    text, fileReadErrorReason = file_option.read_file(fpath)
    # 检查操作代码配置文件是否失败
    if text is None:
        alert.show_alert(fileReadErrorReason)
        return False

    print('\n\n' + sep_line_str)
    # 代码里设置的网络环境
    codeNetType = None
    # 代码里设置的网络环境的那一行内容
    codeNetLine = None
    tl = text.split('\n')
    for line in tl:
        if netStatusForDevCode==line:
            codeNetType = 1
            codeNetLine = line
            break
        elif netStatusForDisCode==line:
            codeNetType = 2
            codeNetLine = line
            break
        elif netStatusForRCCode==line:
            codeNetType = 3
            codeNetLine = line
            break

    if not codeNetLine:
        print('未找到网络设置相关')
        print(sep_line_str + '\n\n')
        return

    if codeNetType == 1:
        print('当前环境：内网')
    elif codeNetType == 2:
        print('当前环境：外网')
    elif codeNetType == 3:
        print('当前环境：RC')

    if netType == codeNetType:
        print('无需更换网络环境代码')
        return

    toReplaceCode = None
    netName = None
    if netType == 1:
        netName = '内网'
        toReplaceCode = netStatusForDevCode
    elif netType == 2:
        netName = '外网'
        toReplaceCode = netStatusForDisCode
    elif netType == 3:
        netName = 'RC'
        toReplaceCode = netStatusForRCCode
    text = text.replace(codeNetLine, toReplaceCode)
    print('已经将网络环境改为了' + netName)

    print(sep_line_str + '\n\n')
    # 写入代码配置文件内容
    fileWriteErrorReason = file_option.write_file(fpath, text)
    # 检查操作失败,弹窗提示
    if fileWriteErrorReason is not None :
        alert.show_alert(fileWriteErrorReason)
        return False
    else :
        return True

def safe_change_podfile_debugmark(selectType, configFilePath, podfileForDebugmode, podfileForReleasemode) :
    filePath = None
    try:
        filePath = settings.kAutoArchiveRepositoryRootPath + configFilePath
        print(filePath)
    except:
        print("未定义代码配置文件!")

    if filePath:
        change_podfile_debugmark(selectType, filePath, podfileForDebugmode, podfileForReleasemode)

# 切换代码中Podefile文件中的DebugMode配置
# selectType:  1,2,3:debugmode 3:releasemode 
# fpath:    代码的配置文件路径
def change_podfile_debugmark(selectType, fpath, podfileForDebugmode, podfileForReleasemode) :
    # 0:release 1:debug
    podDebugmode = 0
    if selectType < 4:
        podDebugmode = 1
    # 获取代码配置文件内容
    text, fileReadErrorReason = file_option.read_file(fpath)
    # 检查操作代码配置文件是否失败
    if text is None:
        alert.show_alert(fileReadErrorReason)
        return False

    print('\n\n' + sep_line_str)
    # 代码里设置
    codeDebugmode = None
    # 代码里设置的网络环境的那一行内容
    codeNetLine = None
    tl = text.split('\n')
    for line in tl:
        if podfileForDebugmode==line:
            codeDebugmode = 1
            codeNetLine = line
            break
        elif podfileForReleasemode==line:
            codeDebugmode = 0
            codeNetLine = line
            break

    if not codeNetLine:
        print('未找到PodDebug设置相关')
        print(sep_line_str + '\n\n')
        return

    if podDebugmode == 0:
        if codeDebugmode == 0:
            print('当前PodDebugMode：OFF')
        else:
            print('当前PodDebugMode：ON')
            text = text.replace(codeNetLine, podfileForReleasemode)
            print('已经PodDebugMode改为了 OFF')
    elif podDebugmode == 1:
        if codeDebugmode == 0:
            print('当前PodDebugMode：OFF')
            text = text.replace(codeNetLine, podfileForDebugmode)
            print('已经PodDebugMode改为了 ON')
        else:
            print('当前PodDebugMode：ON')
    print(sep_line_str + '\n\n')
    # 写入代码配置文件内容
    fileWriteErrorReason = file_option.write_file(fpath, text)
    # 检查操作失败,弹窗提示
    if fileWriteErrorReason is not None :
        alert.show_alert(fileWriteErrorReason)
        return False
    else :
        return True
