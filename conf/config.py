# coding: utf-8

import getpass
import os

####################################################################################################
# 常量配置
####################################################################################################
ConfigInfo_TestDemo = {
    ### 代码工程相关的配置 ###
    # git仓库地址,可空
    'kRepositoryGit': 'git@xxx.xxx/TestDemo.git',
    # 仓库名称(用于区分每个工程)
    'kRepositoryName': 'TestDemo/',
    # 分支名称
    'kBranchName': 'master',
    # Workspace名称(有pod使用.xcworkspace,没有pod使用.xcodeproj)
    'kWorkspaceName':'TestDemo.xcworkspace',
    # Target名称
    'kTargetName': 'TestDemo',
    # AppIcon名称(默认:AppIcon)
    'kAppIconName': 'AppIcon',
}

ConfigInfo_TestDemo2 = {
    ### 代码工程相关的配置 ###
    # git仓库地址,可空
    'kRepositoryGit': 'git@xxx.xxx/TestDemo2.git',
    # 仓库名称(用于区分每个工程)
    'kRepositoryName': 'TestDemo2/',
    # 分支名称
    'kBranchName': 'master',
    # Workspace名称(有pod使用.xcworkspace,没有pod使用.xcodeproj)
    'kWorkspaceName':'TestDemo2.xcworkspace',
    # Target名称
    'kTargetName': 'TestDemo2',
    # AppIcon名称(默认:AppIcon)
    'kAppIconName': 'AppIcon',
}

####################################################################################################
# 其它配置
####################################################################################################

ConfigInfo_General = {
    ### 备份(SMB) ###
    # 是否将 ipa 包拷贝到服务器
    'copy_ipa_to_smb': False, # True, False
    # 服务器地址前缀（需要连接一次这个服务器地址，连接成功后在终端中执行 open / 打开根目录，
    'services_path_prefix': 'smb://192.107.1.1/测试/',
    # 查看是否存在kValidPath的路径,有才可以成功拷贝到服务器,此举为了防止误传,完整的服务器地址为 services_path_prefix + valid_path + v/*.ipa
    'valid_path': '测试安装包/iOS/',

    ### 自动派包(ITC) ###
    # 是否将 ipa 包上传到ITC
    'copy_ipa_to_itc': True, # True, False
    'itc_username': 'aaa@bbb.com',
    'itc_password': 'xxx',

    ### 自动派包(FIR) ###
    # 是否将 ipa 包上传到FIR
    'copy_ipa_to_fir': True, # True, False
    'fir_token': 'xxx',

    ### 自动发邮件 ###
    # 是否发送邮件
    'send_email': True, # True, False
    'email_SMTP': 'smtp.exmail.qq.com',
    'email_SMTP_port': 465,
    'email_user': 'aaa@bbb.com',
    'email_password': 'xxx',
    'email_sender_name': 'iOS Team',
    'email_to_list': ['a001@bbb.com', 'a002@bbb.com'],
    'email_to_list_itc': ['a001@bbb.com'], # ITC上传时可以进行区别配置
    'email_cc_list': None,
}

####################################################################################################
# 脚本配置
####################################################################################################
# 当前配置下标
CurrentConfigIndex = 0
# 所有配置的目录
ConfigDocs = ['TestDemo', 'TestDemo2']
ConfigInfos = [ConfigInfo_TestDemo, ConfigInfo_TestDemo2]

# 调试模式/直接导出ipa包,需要在对应的[DevInner][DevOuter][AppStore]文件夹下放入`.xcarchive`文件
ExportOnly = False   # True, False

####################################################################################################
# 共通方法(以下方法无需要修改)
####################################################################################################

def ConfDocs():
    return ConfigDocs

### 代码工程相关的配置 ###
def kRepositoryGit():
    return ConfigInfos[CurrentConfigIndex]['kRepositoryGit']
def kRepositoryName():
    return ConfigInfos[CurrentConfigIndex]['kRepositoryName']
def kBranchName():
    return ConfigInfos[CurrentConfigIndex]['kBranchName']
def kWorkspaceName():
    return ConfigInfos[CurrentConfigIndex]['kWorkspaceName']
def kTargetName():
    return ConfigInfos[CurrentConfigIndex]['kTargetName']
def kAppIconName():
    return ConfigInfos[CurrentConfigIndex]['kAppIconName']
    
### 自动修改代码的文件,需要自定义 ###
# Podfile中debug模式的切换
def kPodFilePath():
    return kRepositoryName() + 'Podfile'
def kPodfileForReleasemode():
    return 'DebugBranch = DebugBranchReleaseMode'
def kPodfileForDebugmode():
    return 'DebugBranch = DebugBranchDebugMode'
# 主工程中用于切换代码的文件,可注释
def kConfigFilePath():
    return kRepositoryName() + kTargetName() + '/Support/Configs/' + 'Config.h'
def kNetStatusForDisCode():
    return 'static BOOL const APP_MODE_RELEASE = (1);'
def kNetStatusForDevCode():
    return 'static BOOL const APP_MODE_RELEASE = (0);'
### 备份(SMB) ###
def copy_ipa_to_smb():
    return ConfigInfo_General['copy_ipa_to_smb']
def services_path_prefix():
    return ConfigInfo_General['services_path_prefix']
def valid_path():
    return ConfigInfo_General['valid_path']

### 自动派包(ITC) ###
def copy_ipa_to_itc():
    return ConfigInfo_General['copy_ipa_to_itc']
def itc_username():
    return ConfigInfo_General['itc_username']
def itc_password():
    return ConfigInfo_General['itc_password']

### 自动派包(FIR) ###
def copy_ipa_to_fir():
    return ConfigInfo_General['copy_ipa_to_fir']
def fir_token():
    return ConfigInfo_General['fir_token']

### 自动发邮件 ###
def send_email():
    return ConfigInfo_General['send_email']
def email_SMTP():
    return ConfigInfo_General['email_SMTP']
def email_SMTP_port():
    return ConfigInfo_General['email_SMTP_port']
def email_user():
    return ConfigInfo_General['email_user']
def email_password():
    return ConfigInfo_General['email_password']
def email_sender_name():
    return ConfigInfo_General['email_sender_name']
def email_to_list():
    return ConfigInfo_General['email_to_list']
def email_to_list_itc():
    return ConfigInfo_General['email_to_list_itc']
def email_cc_list():
    return ConfigInfo_General['email_cc_list']


