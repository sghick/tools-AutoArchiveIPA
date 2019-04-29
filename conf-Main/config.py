# coding: utf-8

import getpass
import os

####################################################################################################
# 代码工程相关的配置
####################################################################################################

# git仓库地址,可注释
kRepositoryGit = 'git@xxx.xxx/TestDemo.git'
# 仓库名称(用于区分每个工程)
kRepositoryName = 'TestDemo/'
# 分支名称
kBranchName = 'master'
# Workspace名称(有pod使用.xcworkspace,没有pod使用.xcodeproj)
kWorkspaceName = 'TestDemo.xcworkspace'
# Target名称
kTargetName = 'TestDemo'

####################################################################################################
# 自动修改代码的文件,需要自定义
####################################################################################################

# 主工程中用于切换代码的文件,可注释
kConfigFilePath = kRepositoryName + kTargetName + '/' + 'config.h'
kNetStatusForDisCode = '#define APP_RELEASE'
kNetStatusForDevCode = '//#define APP_RELEASE'

####################################################################################################
# 自动派包
####################################################################################################

# 是否将 ipa 包拷贝到服务器
kCopyIpaToServices = False # True, False
# 服务器地址前缀（需要连接一次这个服务器地址，连接成功后在终端中执行 open / 打开根目录，
kServicesPathPrefix = 'smb://192.107.1.1/Test/'
# 查看是否存在kValidPath的路径,有才可以成功拷贝到服务器,此举为了防止误传,完整的服务器地址为 kServicesPathPrefix + kValidPath + v/*.ipa
kValidPath = 'TestPackage/iOS/'

####################################################################################################
# 自动发邮件
####################################################################################################

# 是否发送邮件
send_email = False # True, False
# SMTP及端口配置
email_SMTP = "smtp.exmail.qq.com"
email_SMTP_port = 465
# 邮箱账号
email_user = "iOSTeam@test.com"
# 邮箱密码
email_password = "123456"
# 发件人名称
email_sender_name = 'iOS Team'
# 收件人列表
email_to_list = ['xiaoming@test.com', 'xiaoli@test.com']
# 抄送列表
email_cc_list = None
# 发送主题
email_send_subject = "【自动打包】iOS安装包"

####################################################################################################
# 基本路径的配置-推荐不要修改
####################################################################################################

kPackagePathForConfig = 'conf/'
# 脚本的存放目录,不需要修改
kScriptRootPath = os.getcwd() + '/'
# 源代码存放的根目录,不需要修改
kAutoArchiveRepositoryRootPath = kScriptRootPath + '__repository/'
# 输出文件的根目录,不需要修改
kAutoArchiveExportRootPath = kScriptRootPath + '__export/'

# 输出文件的中间目录(包括AppStore,Dev)
kAutoArchiveExportPath = kScriptRootPath + '__export/' + kRepositoryName
# 输出文件目录及输出配置-AppStore
kExportAppStorePath = kAutoArchiveExportPath + 'AppStore/'
kExportOptionsAppStorePath = kScriptRootPath + kPackagePathForConfig + 'ExportOptions-Dis.plist'
# 输出文件目录及输出配置-dev
kExportDevInnerPath = kAutoArchiveExportPath + 'DevInner/'
kExportDevOuterPath = kAutoArchiveExportPath + 'DevOuter/'
kExportOptionsDevPath = kScriptRootPath + kPackagePathForConfig + 'ExportOptions-Dev.plist'

# '.xcodeproj/.xcworkspace/Podfile'文件所在目录,必须将这些文件放在同一个目录下,用于执行build命令和git命令
cdCommand = 'cd %s' % kAutoArchiveRepositoryRootPath + kRepositoryName
