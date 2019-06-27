# coding: utf-8

from supports import terminal_input
from supports import code_update
from supports import xc_tool
from supports import pod_tool
from supports import send_email
from supports import alert
from supports import print_split
from supports import fir_upload
from conf import config

def main_archive(selectType, cmdType):
    # cmdType: -a:自动上传fir
    # 解析配置类型
    print_split.print_log('1.解析配置类型')
    packageType, netType = terminal_input.parser_select_type(selectType)
    # 切换网络环境
    print_split.print_log('2.切换网络环境')
    code_update.safe_change_code_config_network(netType)
    # 解析打包的输出路径
    print_split.print_log('3.解析打包的输出路径')
    xcarchivePath = terminal_input.parser_xcarchive_path(packageType, netType)
    # 打包归档
    print_split.print_log('4.打包归档')
    archiveSuccess = xc_tool.archive(config.kWorkspaceName, xcarchivePath, config.kTargetName)
    # 如果打包失败,终止之后的操作
    if not archiveSuccess:
        print_split.print_war('打包失败')
        return
    # 读入info配置
    version, build, bundleid, iconpath = xc_tool.readipainfo(xcarchivePath, config.kTargetName)
    # 导出ipa文件,返回ipa文件名(不带扩展名)
    print_split.print_log('5.导出ipa文件')
    exprotFileName, folderPath = xc_tool.exportipa(xcarchivePath, config.kTargetName, packageType, netType, build)
    # 导出dSYM文件
    print_split.print_log('6.导出dSYM文件')
    xc_tool.exportdSYMFile(exprotFileName, folderPath, config.kTargetName)
    # 拷贝到服务器
    localpath = folderPath + exprotFileName + '.ipa'
    status = '本地地址:' + localpath
    showServicesPath = ''
    if config.copy_ipa_to_smb :
        print_split.print_log('7.拷贝到服务器')
        showServicesPath, serviceFileName, alertTitle = xc_tool.uploadService(packageType, netType, exprotFileName, folderPath, build)
        status = status + '\n' + alertTitle
    # 拷贝到FIR
    if config.copy_ipa_to_fir :
        if cmdType == 'a':
            print_split.print_log('8.上传到FIR')
            fir_upload.upload_ipa(folderPath + exprotFileName + '.ipa', folderPath + iconpath, bundleid, netType, version, build)
            status = status + '\n' + "上传FIR成功,请扫码下载"
    # 发邮件
    if config.send_email :
        print_split.print_log('9.发邮件')
        # 打包成功并拷贝到服务器后发送邮件
        email_subject = '【打包成功】' + 'iOS ' + config.kTargetName + " " + build
        email_content = status  
        send_email.send(email_subject , email_content)
    # 结果弹窗
    print_split.print_log('10.结束')
    alert.show_detail_alert("自动打包结束", folderPath, showServicesPath, True)

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
    for s in receiveInput.split(' '):
        selectType = s
        cmdType = ''
        if len(selectType) >= 3:
            selectType = s[:1]
            cmdType = s[2:]
        # 恢复变化
        pod_tool.discardAllChange()
        # 清理缓存
        pod_tool.cleanProject()
        # 进入打包流程
        main_archive(int(selectType), cmdType)

if __name__ == '__main__':
    receiveInput = terminal_input.receive_input()
    archive_ever_input(receiveInput)