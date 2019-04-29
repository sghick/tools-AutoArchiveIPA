# coding: utf-8

from supports import terminal_input
from supports import code_update
from supports import xc_tool
from supports import pod_tool
from supports import send_email
from supports import alert
from conf import config

def main_archive(selectType, selectDebugType):
    # selectDebugType 为 -1，则按照默认约定逻辑；为 0，则强制设置为 Dev 环境；为 1，则则强制设置为 Release 环境；
    # 解析配置类型
    packageType, netType = terminal_input.parser_select_type(selectType)
    # 切换网络环境alert
    code_update.safe_change_code_config_network(netType)
    # 解析打包的输出路径
    xcarchivePath = terminal_input.parser_xcarchive_path(packageType, netType)
    # 打包归档
    archiveSuccess = xc_tool.archive(config.kWorkspaceName, xcarchivePath, config.kTargetName)
    # 如果打包失败,终止之后的操作
    if not archiveSuccess:
        return
    # 导出ipa文件,返回ipa文件名(不带扩展名)
    exprotFileName, folderPath = xc_tool.exportipa(xcarchivePath, config.kTargetName, packageType, netType)
    # 导出dSYM文件
    xc_tool.exportdSYMFile(exprotFileName, folderPath, config.kTargetName)
    # 拷贝到服务器
    showServicesPath, serviceFileName, alertTitle = xc_tool.uploadService(packageType, netType, exprotFileName, folderPath)
    # 发邮件
    send_email.send_success_email(showServicesPath , serviceFileName)
    # 结果弹窗
    alert.show_detail_alert(alertTitle, folderPath, showServicesPath)

def archive_ever_input(receiveInput):
    # 切换打包工程
    if code_update.safe_change_conf_python3(receiveInput.split(' ')) :
        return
    # 下载代码
    pod_tool.git_clone_repository()
    # 更新代码
    pod_tool.updateCode()
    # 下载Podfile中的代码
    pod_tool.installPods()
    # 获取输入信息
    for s in ipts:
        selectType = s
        selectDebugType = -1
        if len(selectType) == 3:
            selectType = s[:1]
            selectDebugType = s[2:]
        # 恢复变化
        pod_tool.discardAllChange()
        # 清理缓存
        pod_tool.cleanProject()
        # 进入打包流程
        main_archive(int(selectType), int(selectDebugType))

if __name__ == '__main__':
    receiveInput = terminal_input.receive_input()
    archive_ever_input(receiveInput)