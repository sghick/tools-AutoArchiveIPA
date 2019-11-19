# coding: utf-8

import sys
from supports import terminal_input
from supports import code_update
from supports import xc_tool
from supports import pod_tool
from supports import auto_smb
from supports import auto_itc
from supports import auto_fir
from supports import auto_email
from utils import alert
from utils import print_split
from conf import config

def main_archive(selectType, cmdType):
    # config values
    config_ExportOnly = config.ExportOnly

    config_kRepositoryGit = config.kRepositoryGit()
    config_kRepositoryName = config.kRepositoryName()
    config_kBranchName = config.kBranchName()
    config_kWorkspaceName = config.kWorkspaceName()
    config_kTargetName = config.kTargetName()
    config_kAppIconName = config.kAppIconName()

    config_kPodFilePath = config.kPodFilePath()
    config_kPodfileForDebugmode = config.kPodfileForDebugmode()
    config_kPodfileForReleasemode = config.kPodfileForReleasemode()
    
    config_kConfigFilePath = config.kConfigFilePath()
    config_kNetStatusForDisCode = config.kNetStatusForDisCode()
    config_kNetStatusForDevCode = config.kNetStatusForDevCode()
    
    config_copy_ipa_to_smb = config.copy_ipa_to_smb()
    config_services_path_prefix = config.services_path_prefix()
    config_configvalid_path = config.valid_path()
    config_copy_ipa_to_itc = config.copy_ipa_to_itc()
    config_itc_username = config.itc_username()
    config_itc_password = config.itc_password()
    config_copy_ipa_to_fir = config.copy_ipa_to_fir()
    config_fir_token = config.fir_token()
    config_send_email = config.send_email()
    config_email_SMTP = config.email_SMTP()
    config_email_SMTP_port = config.email_SMTP_port()
    config_email_user = config.email_user()
    config_email_password = config.email_password()
    config_email_sender_name = config.email_sender_name()
    config_email_to_list = config.email_to_list()
    config_email_to_list_itc = config.email_to_list_itc()
    config_email_cc_list = config.email_cc_list()

    # cmdType: -a:自动上传fir
    # 解析配置类型
    print_split.print_log('1.解析配置类型')
    packageType, netType = terminal_input.parser_select_type(selectType)

    # 非调试模式时
    if config.ExportOnly==False:
        # 恢复变化
        pod_tool.discardAllChange(config.kRepositoryName())
        # 下载代码
        pod_tool.git_clone_repository(config.kRepositoryGit())
        # 更新代码
        pod_tool.updateCode(config.kRepositoryName(), config.kBranchName())
        # 校验podfile的debugmode
        code_update.safe_change_podfile_debugmark(selectType, config_kPodFilePath, config_kPodfileForDebugmode, config_kPodfileForReleasemode)
        # 下载Podfile中的代码
        pod_tool.installPods(config.kRepositoryName())
        # 清理缓存
        pod_tool.cleanProject(config.kRepositoryName(), config.kTargetName())

    # 切换网络环境
    print_split.print_log('2.切换网络环境')
    code_update.safe_change_code_config_network(netType, config_kConfigFilePath, config_kNetStatusForDevCode, config_kNetStatusForDisCode)
    # 解析打包的输出路径
    print_split.print_log('3.解析打包的输出路径')
    xcarchivePath = terminal_input.parser_xcarchive_path(config_kRepositoryName, packageType, netType)
    # 打包归档
    if config.ExportOnly==False:
        print_split.print_log('4.打包归档')
        archiveSuccess = xc_tool.archive(config_kRepositoryName, config_kWorkspaceName, xcarchivePath, config_kTargetName)
        # 如果打包失败,终止之后的操作
        if not archiveSuccess:
            print_split.print_war('打包失败')
            return
    # 读入info配置
    version, build, bundleid, iconpath = xc_tool.readipainfo(xcarchivePath, config_kTargetName, config_kAppIconName)
    # 导出ipa文件,返回ipa文件名(不带扩展名)
    print_split.print_log('5.导出ipa文件')
    exprotFileName, folderPath = xc_tool.exportipa(config_kRepositoryName, xcarchivePath, config_kTargetName, packageType, netType, build)
    # 导出dSYM文件
    print_split.print_log('6.导出dSYM文件')
    xc_tool.exportdSYMFile(exprotFileName, folderPath, config_kTargetName)
    # 备份
    localpath = folderPath + exprotFileName + '.ipa'
    status = print_split.get_log('打包成功')
    status = status + '\n' + '本地地址:\n  ' + localpath

    showServicesPath = ''
    if config_copy_ipa_to_smb :
        print_split.print_log('7.备份到SMB')
        showServicesPath, serviceFileName, alertTitle = auto_smb.uploadipa(config_services_path_prefix, config_valid_path, packageType, netType, exprotFileName, folderPath, build)
        status = status + '\n' + alertTitle
    # 自动上传/派包
    if cmdType == 'a':
        # 上传到ITC
        if selectType == 3:
            if config_copy_ipa_to_itc :
                print_split.print_log('8.上传到ITC(appstore类型专属)')
                auto_itc.uploaditc(localpath, config_itc_username, config_itc_password)
                status = status + '\n' + print_split.get_log('已经上传至ITC')
                status = status + '\n' + '是否上传成功,请以苹果邮件和具体情况为准,成功后可进行testflight测试'
        # 上传到FIR
        else:
            if config_copy_ipa_to_fir :
                print_split.print_log('9.上传到FIR')
                downloadurl, operalurl = auto_fir.upload_ipa(config_fir_token, localpath, folderPath + iconpath, bundleid, netType, version, build)
                status = status + '\n' + print_split.get_log('上传FIR成功')
                status = status + '\n' + '请扫码下载:'
                status = status + '\n' + '操作地址:\n  ' + operalurl
                status = status + '\n' + '下载地址:\n  ' + downloadurl
    # 结果
    if config_send_email :
        email_to_list = config_email_to_list if selectType != 3 else config_email_to_list_itc
        # 发邮件
        print_split.print_log('10.发邮件')
        # 打包成功并拷贝到服务器后发送邮件
        se = auto_email.email_create(config_email_SMTP, config_email_SMTP_port, config_email_user, config_email_password)
        email_subject = '【打包成功】' + 'iOS ' + config_kTargetName + ' ' + build + ' ' + terminal_input.parser_net_name(selectType)
        email_content = status  
        auto_email.send(se, config_email_sender_name, email_to_list, config_email_cc_list, email_subject, email_content)
    else:
        # 结果弹窗
        print_split.print_log('11.结束')
        alert.show_detail_alert('自动打包结束', folderPath, showServicesPath, True)

def begin_tip(rinputs):
    print_split.print_log('即将开始打包')
    print_split.print_war('当前项目名:' + config.kTargetName())
    print_split.print_war('当前分支:' + config.kBranchName())

def valid_inputs(rinpts):
    if len(rinpts)==0:
        return False
    # 带'-'的命令可以通过
    if rinpts[0][:1]=='-':
        try:
            rinpts[0][1:2]=='e'
            return True
        except:
            return False

    for s in rinpts:
        selectType = s
        if len(selectType) >= 3:
            selectType = s[:1]
        try:
            if int(selectType) > 3:
                return False
        except:
            return False
    return True

def archive_ever_input(rinpts):
    # 参数校验
    if valid_inputs(rinpts)==False :
        print_split.print_war('参数错误~') 
        return 
    # 切换打包工程
    if code_update.safe_change_conf_python3(rinpts, config.ConfDocs())==False :
        return
    # 即将打包提示
    begin_tip(rinpts)
    # 获取输入信息
    for s in rinpts:
        selectType = s
        cmdType = ''
        if len(selectType) >= 3:
            selectType = s[:1]
            cmdType = s[2:]
        # 进入打包流程
        main_archive(int(selectType), cmdType)

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        receiveInput = terminal_input.receive_input(config.kBranchName(), config.kTargetName(), config.ConfDocs())
        rinpts = receiveInput.split(' ')
        print(rinpts[0])
        archive_ever_input(rinpts)
    else:
        rinpts = args[1:len(args)]
        print(rinpts[0])
        archive_ever_input(rinpts)