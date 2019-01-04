# coding: utf-8

from supports import file_option
from supports import alert
from conf import config

sep_line_str = '+----------------------------+'

####################################################################################################
# 更改代码配置
####################################################################################################

def safe_change_code_config_network(netType) :
    filePath = None
    try:
        filePath = config.kAutoArchiveRepositoryRootPath + config.kConfigFilePath
        print(filePath)
    except:
        print("未在config.py中定义代码配置文件!")

    
    if not filePath:
        change_code_config_network(netType, filePath)

# 切换代码中配置文件的网络环境配置
# netType:  1:内网,2:外网
# fpath:    代码的配置文件路径
def change_code_config_network(netType, fpath) :
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
        if config.kNetStatusForDevCode==line:
            codeNetType = 1
            codeNetLine = line
            break
        elif config.kNetStatusForDisCode==line:
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
            text = text.replace(codeNetLine, config.kNetStatusForDevCode)
            print('已经将环境改为了内网')
    elif netType == 2:
        if codeNetType == 1:
            print('当前环境：内网')
            text = text.replace(codeNetLine, config.kNetStatusForDisCode)
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