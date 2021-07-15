# coding: utf-8

import getpass
import os

class ProjectItem:
    def __init__(self):
        self.scheme = 'Runner'
        # 工程名(cocoas pod 创建)
        self.workspace = 'Runner.xcworkspace'
        # 打包配置输入文件夹(ExportOptions.plist文件)
        self.inputDoc = './release_conf/'
        # 打包输入文件夹
        self.outputDoc = '../../release/'
        # Icon名字
        self.appIconName = 'AppIcon60x60@3x.png'

class ItcItem:
    def __init__(self):
        self.username = 'xxx@xxxxx.com'
        self.password = 'xxxx-xxxx-xxxx-xxxx'

class FirItem:
    def __init__(self):
        self.token = 'xxxxxxxx'

class EmailItem:
    def __init__(self):
        self.smtp = 'smtp.exmail.qq.com'
        self.port = 465
        self.user = 'xxxx@xxxxx.com'
        self.password = 'xxx'
        self.sendername = 'iOS Team'
        self.tolist = ['xxx@xxxx.com', 'yyy@xxxx.com']
        self.toitclist = ['xxx@xxxx.com', 'zzz@xxxx.com']
        self.cclist = None

class CodeItem:
    def __init__(self):
        self.path = None
        self.release = None
        self.dev = None

    def flutterCode(self):
        item = CodeItem()
        item.path = '../lib/config.dart'
        item.release = 'bool get appReleaseMode => true;'
        item.dev = 'bool get appReleaseMode => false;'
        return item

    def ocCode(self):
        item = CodeItem()
        item.path = './Runner/BDSSupport/Configs/BDSConfig.h'
        item.release = 'static NSInteger const APP_MODE_RELEASE = (1);'
        item.dev = 'static NSInteger const APP_MODE_RELEASE = (0);'
        return item

    def podCode(self):
        item = CodeItem()
        item.path = './Podfile'
        item.release = 'BDSDebugMode = BDSDebugBranchReleaseMode'
        item.dev = 'BDSDebugMode = BDSDebugBranchDebugMode'
        return item

class ConfigInfo:
    def __init__(self):
        self.proItem = ProjectItem()
        self.itcItem = ItcItem()
        self.firItem = FirItem()
        self.emailItem = EmailItem()
        self.flutterCode = CodeItem().flutterCode()
        self.ocCode = CodeItem().ocCode()
        self.podCode = CodeItem().podCode()



