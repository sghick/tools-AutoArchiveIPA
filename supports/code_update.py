# coding: utf-8

from utils import file_option
from utils import alert
from utils import settings

sep_line_str = '+----------------------------+'

####################################################################################################
# 更改打包配置
####################################################################################################

def safe_change_conf_python3(inputs, confDocs) :
    fmt = inputs[0][0]
    idx = inputs[0][1:]

    if (fmt == 'e') :
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
        print('未找到配置!')
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

def safe_change_code_config_network(netType, configFilePath, netStatusForDevCode, netStatusForDisCode) :
    filePath = None
    try:
        filePath = settings.kAutoArchiveRepositoryRootPath + configFilePath
        print(filePath)
    except:
        print("未定义代码配置文件!")

    if filePath:
        change_code_config_network(netType, filePath, netStatusForDevCode, netStatusForDisCode)

# 切换代码中配置文件的网络环境配置
# netType:  1:内网,2:外网
# fpath:    代码的配置文件路径
def change_code_config_network(netType, fpath, netStatusForDevCode, netStatusForDisCode) :
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

    if not codeNetLine:
        print('未找到网络设置相关')
        print(sep_line_str + '\n\n')
        return

    if netType == 1:
        if codeNetType == 1:
            print('当前环境：内网')
        else:
            print('当前环境：外网')
            text = text.replace(codeNetLine, netStatusForDevCode)
            print('已经将环境改为了内网')
    elif netType == 2:
        if codeNetType == 1:
            print('当前环境：内网')
            text = text.replace(codeNetLine, netStatusForDisCode)
            print('已经将环境改为了外网')
        else:
            print('当前环境：外网')
    print(sep_line_str + '\n\n')
    # 写入代码配置文件内容
    fileWriteErrorReason = file_option.write_file(fpath, text)
    # 检查操作失败,弹窗提示
    if fileWriteErrorReason is not None :
        alert.show_alert(fileWriteErrorReason)
        return False
    else :
        return True
