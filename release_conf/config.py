# coding: utf-8

import getpass
import os

####################################################################################################
# 常量配置
####################################################################################################
ConfigInfo_Proj = {
    ### 代码工程相关的配置 ###
    # 项目Target名字
    'scheme': 'xiaomi',
    # 工程名(cocoas pod 创建)
    'workspace': 'xiaomi.xcworkspace',
    # 打包配置输入文件夹(ExportOptions.plist文件)
    'inputDoc': './lite-release/',
    # 打包输入文件夹
    'outputDoc':'../../xiaomi_output/',
    # Icon名字
    'appIconName': 'AppIcon60x60@3x.png',
}

####################################################################################################
# 其它配置
####################################################################################################

ConfigInfo_General = {
    ### 自动派包(ITC) ###
    'itc_username': 'xxx@xxxx.com',
    'itc_password': 'xxxx-xxxx-xxxx-xxxx',

    ### 自动派包(FIR) ###
    'fir_token': 'xxxxx',

    ### 自动发邮件 ###
    # 是否发送邮件
    'email_SMTP': 'smtp.exmail.qq.com',
    'email_SMTP_port': 465,
    'email_user': 'xxx@xxxx.com',
    'email_password': 'xxxxx',
    'email_sender_name': 'iOS Team',
    'email_to_list': ['xiaomi@xxxx.com', 'xiaohong@xxxx.com',
    'email_to_list_itc': ['xiaomi@xxxx.com', 'xiaohua@xxxx.com'],
    'email_cc_list': None,
}

####################################################################################################
# 共通方法
####################################################################################################

### 代码工程相关的配置 ###
def kScheme():
    return ConfigInfo_Proj['scheme']
def kWorkspace():
    return ConfigInfo_Proj['workspace']
def kInputDoc():
    return ConfigInfo_Proj['inputDoc']
def kOutputDoc():
    return ConfigInfo_Proj['outputDoc']
def kAppIconName():
    return ConfigInfo_Proj['appIconName']

### 自动修改代码的文件,需要自定义 ###
def code_path():
    return '../lib/config.dart'
def dev_code():
    return 'bool get appReleaseMode => false;'
def release_code():
    return 'bool get appReleaseMode => true;'

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


