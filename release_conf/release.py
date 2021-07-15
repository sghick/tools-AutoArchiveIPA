# coding: utf-8
# 本脚本copy到工程目录下,与工程文件同级即可

import sys
import time
import re
import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from release_conf import config

# @params selectType 1:dev-test,2:dev-online,3:rc-online,4:AppStore-online
# @params cmdType -a 自动上传至Fir/AppStore
def main_archive(selectType, cmdType):
    print(_cmd_string(selectType, cmdType))
    conf = config.ConfigInfo().proItem
    ### config
    scheme = conf.scheme
    workspace = conf.workspace
    inputDoc = conf.inputDoc
    outputDoc = conf.outputDoc
    appIconName = conf.appIconName
    # 状态变量
    subject = ''
    content = ''
    xcarchiveOutput = _xcarchive_output(selectType, outputDoc)
    # 打包归档
    archiveSuccess, xcarchiveFilePath = archive(workspace, scheme, xcarchiveOutput)
    # 如果打包失败,终止之后的操作
    if not archiveSuccess:
        content = 'archive faild ==> ' + _cmd_string(selectType, cmdType)
        subject = '打包失败'
    else:
        # 读入info配置
        version, build, bundleId, iconFile = read_ipa_info(xcarchiveFilePath, appIconName)
        print(version + '\n' + build + '\n' + bundleId + '\n' + iconFile)
        # 导出ipa文件
        exportOptionsFilePath = _xcexport_input(selectType, inputDoc, scheme)
        exportSuccess, folderPath, exprotFileName, newXcarchiveFilePath = export_ipa(xcarchiveOutput, scheme, selectType, version, exportOptionsFilePath)
        if not exportSuccess:
            content = 'export faild ==> ' + _cmd_string(selectType, cmdType)
            subject = '导出失败'
        else:
            # 拼ipa文件路径
            ipaPath = folderPath + exprotFileName + '.ipa'
            # 导出dSYM文件
            export_dSYM_file(folderPath, exprotFileName, scheme)
            # 成功才会往下走,失败则抛出异常
            content = content + '\n' + '======= 打包成功 ======='
            content = content + '\n' + 'ipaPath:%s' % ipaPath
            subject = '打包成功'
            print(content)
            # 自动上传/派包
            if cmdType == 'a':
                # 上传到ITC
                if selectType == 4:
                    _uploadToAppStore(ipaPath)
                    content = content + '\n' + '======= 已经上传至ITC ======='
                    content = content + '\n' + '是否上传成功,请以苹果邮件和具体情况为准,成功后可进行testflight测试'
                # 上传到FIR
                else:
                    iconPath = newXcarchiveFilePath + iconFile
                    downloadurl, operalurl = _uploadToFir(selectType, ipaPath, iconPath, bundleId, version, build)
                    content = content + '\n' + '======= 上传FIR成功 ======='
                    content = content + '\n' + '请扫码下载:'
                    content = content + '\n' + '操作地址:\n  ' + operalurl
                    content = content + '\n' + '下载地址:\n  ' + downloadurl
            else:
                content = content + '\n' + '======= 未选择自动上传 ======='
                content = content + '\n' + '如需自动上传,请在加上命令参数 -a'
    if cmdType == 'a':
        _sendEmail(selectType, subject, content)
    print(content)

# 根据输入类型和配置信息,返回xc打包路径
def _xcarchive_output(selectType, root):
    ### config
    if selectType == 1:
        return '%sDevInner/' % root
    elif selectType == 2:
        return '%sDevOuter/' % root
    elif selectType == 3:
        return '%sDevRC/' % root
    elif selectType == 4:
        return '%sAppStore/' % root
    return ''

def _xcexport_input(selectType, root, scheme):
    ### config
    filename = 'ExportOptions.plist'
    if selectType == 1:
        return '%s%s-Dev-%s' % (root, scheme, filename)
    elif selectType == 2:
        return '%s%s-Dev-%s' % (root, scheme, filename)
    elif selectType == 3:
        return '%s%s-Dev-%s' % (root, scheme, filename)
    elif selectType == 4:
        return '%s%s-Dis-%s' % (root, scheme, filename)
    return ''

def _uploadToAppStore(ipaPath):
    conf = config.ConfigInfo().itcItem
    uploaditc(ipaPath, conf.username, conf.password)

def _uploadToFir(selectType, ipaPath, iconPath, bundleId, version, build):
    conf = config.ConfigInfo().firItem
    fir_token = conf.token
    changelog = _fir_changelog(selectType)
    downloadurl, operalurl = upload_ipa(fir_token, ipaPath, iconPath, bundleId, version, build, changelog)
    return downloadurl, operalurl

def _sendEmail(selectType, subject, content):
    conf = config.ConfigInfo().emailItem
    email_SMTP = conf.smtp
    email_SMTP_port = conf.port
    email_user = conf.user
    email_password = conf.password
    email_sender_name = conf.sendername
    email_to_list = conf.tolist
    email_to_list_itc = conf.toitclist
    email_cc_list = conf.cclist
    # 
    email_to_list = email_to_list if selectType != 4 else email_to_list_itc
    # 打包成功并拷贝到服务器后发送邮件
    se = email_create(email_SMTP, email_SMTP_port, email_user, email_password)
    email_subject = subject
    email_content = content  
    email_send(se, email_sender_name, email_to_list, email_cc_list, email_subject, email_content)

####################################################################################################
# String
####################################################################################################

def _parser_selectType(selectType):
    nn = None
    pn = None
    if selectType == 1:
        return '内网', 'Dev'
    if selectType == 2:
        return '外网', 'Dev'
    if selectType == 3:
        return 'RC', 'Dev'
    if selectType == 4:
        return '外网', 'Dis'
    return nn, pn

def _parser_net_name(selectType):
    netname = ''
    if selectType == 1:
        netname = 'Dev包测试环境'
    elif selectType == 2:
        netname = 'Dev包线上环境'
    elif selectType == 3:
        netname = 'Dev包RC环境'
    elif selectType == 4:
        netname = 'AppStore包'
    return netname

def _fir_changelog(selectType):
    changelog = ''
    if selectType == 1:
        changelog = '[测试环境](脚本自动上传,请添加更新说明)'
    elif selectType == 2:
        changelog = '[线上环境](脚本自动上传,请添加更新说明)'
    elif selectType == 3:
        changelog = '[RC环境](脚本自动上传,请添加更新说明)'
    else:
        changelog = '(脚本自动上传,请添加更新说明)'
    return changelog

def _cmd_string(selectType, cmdType):
    return 'selectType:%d, cmdType:%s' % (selectType, cmdType)

####################################################################################################
# Archve
####################################################################################################

# archive并导出ipa
def archive(workspace, scheme, outputPath) :
    xcarchiveFilePath = '%s%s.xcarchive' % (outputPath, scheme)
    archiveCommand = "xcodebuild archive -destination 'generic/platform=iOS' -workspace '%s' -scheme '%s' -archivePath '%s' -quiet" % (workspace, scheme, xcarchiveFilePath)
    cdCommand = 'cd %s' % './'
    print('archiveCommand：' + archiveCommand)
    os.system('%s' % cdCommand + ';' + archiveCommand)

    # 检查 archive 是否成功
    if os.path.exists(xcarchiveFilePath) is False:
        return False, ''
    return True, xcarchiveFilePath

# 读入info配置
def read_ipa_info(xcarchiveFilePath, appIconName):
    infoplistpath = xcarchiveFilePath + '/Info.plist'
    iconFile = '/Products/%s/%s' % (getApplicationPath(infoplistpath), appIconName)
    version = getShortVersion(infoplistpath)
    build = getVersion(infoplistpath)
    bundleId = getBundleID(infoplistpath)
    return version, build, bundleId, iconFile

def export_ipa(exportPath, targetName, selectType, v, exportOptionsFilePath):
    curTime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    folderName = '%s %s' % (targetName, curTime)
    folderPath = '%s%s/%s/' % (exportPath, v, folderName)
    createFolderIfNeed(folderPath)
    # 找到 .xcarchive 文件
    xcarchiveFileName = targetName + '.xcarchive'
    xcarchiveFilePath = exportPath + xcarchiveFileName
    # ExportOptions-xxx.plist 文件
    if not os.path.exists(exportOptionsFilePath) :
        return False, '', '', ''
    # 导出ipa包
    exportArchiveCommand = "xcodebuild -exportArchive -archivePath '%s' -exportPath '%s' -exportOptionsPlist '%s'" % (
    xcarchiveFilePath, folderPath, exportOptionsFilePath)
    print('exportArchiveCommand：' + exportArchiveCommand)
    os.system(exportArchiveCommand)
    ipaFilePath = folderPath + getFilePath(folderPath, '.ipa')
    # 检查导出 ipa 是否成功
    if os.path.exists(ipaFilePath) is False:
        print(ipaFilePath)
        return False, '', '', ''
    # 把 ipa 包重新命名下
    nn, pn = _parser_selectType(selectType)
    exprotFileName = targetName + '-' + v + '-' + nn + '-' + pn
    newIpaFilePath = folderPath + '/' + exprotFileName + '.ipa'
    fileRename(ipaFilePath, newIpaFilePath)
    # 导出成功后再移动 .xcarchive 文件到新目录中
    newXcarchiveFilePath = folderPath + xcarchiveFileName
    moveFileToFolder(xcarchiveFilePath, newXcarchiveFilePath)
    return True, folderPath, exprotFileName, newXcarchiveFilePath

def export_dSYM_file(folderPath, exprotFileName, scheme):
    # .dSYM 文件到新目录中
    dSYMPath = folderPath + scheme + '.xcarchive/dSYMs/' + scheme.lower() + '.app.dSYM'
    dSYMToOutputPath = folderPath + exprotFileName + '.dSYM'
    print('dSYM:' + dSYMPath)
    print('dSYM out put:' + dSYMToOutputPath)
    copyFolderToFolder(dSYMPath, dSYMToOutputPath)

####################################################################################################
# 文件操作的定义
####################################################################################################

# 根据传入的文件路径，获取这个文件的文本内容
def read_file(fpath) :
    f = None
    # 文件内容
    text = None
    fileReadErrorReason = None
    try:
        # 打开文件
        f = open(fpath, 'r')
        # 读取文件
        text = f.read()
    except Exception as e:
        fileError = True
        fileReadErrorReason = '读取[' + fpath + ']文件出错！'
        print(fileReadErrorReason)
        print(e)
    finally:
         # 关闭文件
        if f:
            f.close()
        return text, fileReadErrorReason

# 根据传入的文件路径,替换写入text内容
def write_file(fpath, text) :
    fileWriteErrorReason = None
    try:
        # 打开文件
        f = open(fpath, 'w')
        # 写入文件
        f.write(text)
    except Exception as e:
        fileWriteErrorReason = '写入[' + fpath + ']文件出错！'
        print(fileWriteErrorReason)
        print(e)
    finally:
        # 关闭文件
        if f:
            f.close()
    return fileWriteErrorReason


####################################################################################################
# 文件&文件夹操作
####################################################################################################

def copyFileToFolder(filePath, folderPath):
    cmd = "cp '%s' '%s'" % (filePath, folderPath)
    os.system(cmd)

def copyFolderToFolder(folderPath1, folderPath2):
    cmd = "cp -R '%s' '%s'" % (folderPath1, folderPath2)
    os.system(cmd)

def removeFolder(folderPath):
    cmd = "rm -rf '%s'" % folderPath
    os.system(cmd)

def moveFileToFolder(filePath, folderPath):
    cmd = "mv '%s' '%s'" % (filePath, folderPath)
    os.system(cmd)

def fileRename(oldFilePath, newFilePath):
    cmd = "mv '%s' '%s'" % (oldFilePath, newFilePath)
    os.system(cmd)

def createFolderIfNeed(folderPath):
    cmd = "mkdir -p '%s'" % folderPath
    os.system(cmd)

def getFilePath(folderPath, pattern):
    files = os.listdir(folderPath)
    for i in files:
        if i.endswith(pattern):
            return i

####################################################################################################
# 从 info.plist 获取版本号
####################################################################################################

def getVersionWithKey(key, fpath):
    f = None
    # 文件内容
    text = None
    try:
        # 打开文件
        f = open(fpath, 'r')
        # 读取文件
        text = f.read()
        l = text.split('\n')
        v = None
        flage = False
        for line in l:
            if flage:
                lstripline = line.lstrip()
                start = len('<string>')
                end = len('</string>')
                v = lstripline[start:-end]
                break
            else:
                if key in line:
                    flage = True
        return v
    except Exception as e:
        print('读取 %s 文件出错！', fpath)
        print(e)
    finally:
        # 关闭文件
        if f:
            f.close()

def getShortVersion(fpath):
    return getVersionWithKey('CFBundleShortVersionString', fpath)

def getVersion(fpath):
    return getVersionWithKey('CFBundleVersion', fpath)

def getBundleID(fpath):
    return getVersionWithKey('CFBundleIdentifier', fpath)

def getApplicationPath(fpath):
    return getVersionWithKey('ApplicationPath', fpath)

####################################################################################################
# itc upload:https://help.apple.com/itc/apploader/#/apdATD1E53-D1E1A1303-D1E53A1126
####################################################################################################

def validateipa(filepath, username, password):
    print('ITC验证app:')
    toolcmd = 'xcrun altool'
    command = "%s --validate-app -f '%s' -t ios -p '%s' -u '%s'" % (toolcmd, filepath, password, username)
    print('altoolValidateCommand：' + command)
    os.system(command)
    return

def uploadipa(filepath, username, password):
    print('ITC上传app:')
    toolcmd = 'xcrun altool'
    command = "%s --upload-app -f '%s' -t ios -p '%s' -u '%s'" % (toolcmd, filepath, password, username)
    print('altoolUploadCommand：' + command)
    os.system(command)
    return

def uploaditc(filepath, username, password):
    validateipa(filepath, username, password)
    uploadipa(filepath, username, password)
    return

####################################################################################################
# Fir
####################################################################################################

# 获取 fir 的上传凭证
def get_cert(bundle_id, api_token):
    print('发起获取上传凭证请求 ========')
    data = {'type': 'ios', 'bundle_id': bundle_id,
            'api_token': api_token}
    print(data)
    req = requests.post(url='http://api.bq04.com/apps', data=data)
    cert_resp = req.content
    print('获取到 fir 响应 ========')
    print(str(cert_resp))
    return cert_resp

# 上传到icon到fir
def upload_icon(icon, path):
    # 拿到相应的token
    cert_key = icon['key']
    cert_token = icon['token']
    cert_upload_url = icon['upload_url']

    print('上传 icon ========')
    file = {'file': open(path, 'rb')}
    param = {
        "key": cert_key,
        "token": cert_token
    }
    requests.packages.urllib3.disable_warnings()
    req = requests.post(cert_upload_url,files=file, data=param, verify=False)
    print(req.content)
    return req.content

# 上传到ipa到fir
def upload_fir(binary, path, version, build, changelog):
    # 拿到相应的token
    cert_key = binary['key']
    cert_token = binary['token']
    cert_upload_url = binary['upload_url']

    print('上传 iPA ========')
    file = {'file': open(path, 'rb')}
    param = {
        "key": cert_key,
        "token": cert_token,
        "x:version": version,
        "x:build": build,
        "x:changelog": changelog
    }
    requests.packages.urllib3.disable_warnings()
    req = requests.post(cert_upload_url,files=file, data=param, verify=False)
    print(req.content)
    return req.content

def upload_ipa(fir_token, ipa_path, iconpath, bundle_id, version, build, changelog):
    cert_resp2 = get_cert(bundle_id, fir_token)
    cert_json = json.loads(cert_resp2)
    binary_dirt = cert_json['cert']['binary']
    icon_dirt = cert_json['cert']['icon']
    downloadurl = 'http://d.firim.info/' + cert_json['short']
    operalurl = 'https://www.betaqr.com/apps/' + cert_json['id']
    upload_icon(icon_dirt, iconpath)
    upload_fir(binary_dirt, ipa_path, version, build, changelog)
    return downloadurl, operalurl

####################################################################################################
# 邮件操作
####################################################################################################

class SendEmail:
    def __init__(self):
        self.SMTP = None
        self.port = None
        self.user = None
        self.passwd = None
        self.sender_name = None
        self.to_list = []
        self.cc_list = []
        self.subject = None
        self.content = None
        self.doc = None

    def send(self):
        '''
        发送邮件
        '''
        print('邮件发送中...')
        try:
            server = smtplib.SMTP_SSL(self.SMTP, port=self.port)
            server.login(self.user, self.passwd)
            server.sendmail("<%s>" % self.user, self.to_list + self.cc_list, self.get_attach())
            server.close()
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败")
            print(e)

    def get_attach(self):
        '''
        构造邮件内容
        '''
        attach = MIMEMultipart()
        if self.content is not None:
            # 添加邮件内容
            txt = MIMEText(self.content)
            attach.attach(txt)
        if self.subject is not None:
            # 主题,最上面的一行
            attach["Subject"] = self.subject
        if self.user is not None:
            # 显示在发件人
            attach["From"] = self.sender_name + "<%s>" % self.user
        if self.to_list:
            # 收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            # 抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            # 估计任何文件都可以用base64，比如rar等
            # 文件名汉字用gbk编码代替
            name = os.path.basename(self.doc).encode("gbk")
            f = open(self.doc, "rb")
            doc = MIMEText(f.read(), "base64", "gb2312")
            doc["Content-Type"] = 'application/octet-stream'
            doc["Content-Disposition"] = 'attachment; filename="' + name + '"'
            attach.attach(doc)
            f.close()
        return attach.as_string()

def email_create(SMTP, port, user, password):
    se = SendEmail()
    se.SMTP = SMTP
    se.port = port
    se.user = user
    se.passwd = password
    return se

def email_send(se, sendername, to_list, cc_list, subject, content):
    se.sender_name = sendername
    se.to_list = to_list
    if cc_list:
        se.cc_list = cc_list
    # 主题
    se.subject = subject
    # 内容
    se.content = '\n' + content
    # 附件
    # se.doc = '填写一个文件路径'
    se.send()

####################################################################################################
# for code change
####################################################################################################

def change_flutter_code(selectType, isflutter):
    rtn = True
    conf = config.ConfigInfo()
    if isflutter:
        rtn = replaceCode(selectType, conf.flutterCode)
    else:
        rtn = replaceCode(selectType, conf.ocCode)
    replaceCode(selectType, conf.podCode)
    return rtn

####################################################################################################
# for file replace
####################################################################################################   

def replaceCode(selectType, codeItem):
    ### config
    code_path = codeItem.path
    dev_code = codeItem.dev
    release_code = codeItem.release

    # 切换环境代码
    text, fileReadErrorReason = read_file(code_path)
    # 检查操作代码配置文件是否失败
    if text is None:
        print(fileReadErrorReason)
        return False
    success, newText = replace_project_code(text, selectType, dev_code, release_code)
    if success == False:
        print('替换网络环境代码失败:selectType:' + str(selectType))
        return False
        # 写入代码配置文件内容
    fileWriteErrorReason = write_file(code_path, newText)
    # 检查操作失败,弹窗提示
    if fileWriteErrorReason is not None :
        print(fileWriteErrorReason)
        return False
    else :
        return True

def replace_project_code(text, selectType, devCode, releaseCode):
    replaceCode = code_for_replace(selectType, devCode, releaseCode)
    tl = text.split('\n')
    currentCode = ''
    for line in tl:
        print(line)
        if devCode==line:
            currentCode = line
            break
        elif releaseCode==line:
            currentCode = line
            break
    if currentCode == '':
        print('未找到配置文件')
        return False, text
    if currentCode == replaceCode:
        print('当前环境配置无需切换:%s' % currentCode)
    else:
        print('当前环境配置:%s, 需要切换至:%s' % (currentCode, replaceCode))
        text = text.replace(currentCode, replaceCode)
    return True, text
    
def code_for_replace(selectType, devCode, releaseCode):
    if selectType == 2:
        return releaseCode
    elif selectType == 3:
        return releaseCode
    elif selectType == 4:
        return releaseCode
    return devCode

####################################################################################################
# __main__
####################################################################################################
def _archive_ever_input(rinpts):
    isflutter = False
    finputs = rinpts
    if len(rinpts) > 0:
        if rinpts[0] == 'flutter':
            isflutter = True
            finputs = rinpts[1:]
    for s in finputs:
        selectType = s
        cmdType = ''
        if len(selectType) >= 3:
            selectType = s[:1]
            cmdType = s[2:]
        # flutter打包模式切换环境
        if change_flutter_code(int(selectType), isflutter):
            if isflutter:
                # build ios
                os.system('flutter build ios')
            # 进入打包流程
            main_archive(int(selectType), cmdType)

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('+----------------------------+')
        print('+----------------------------+')
        print('|' + _parser_net_name(1) + '请输: 1')
        print('|' + _parser_net_name(2) + '请输: 2')
        print('|' + _parser_net_name(3) + '请输: 3')
        print('|' + _parser_net_name(4) + '请输: 4')
        print('+----------------------------+')
        print('|打flutter项目的包请在数字前增加flutter标识,如flutter 1-a')
        print('|打多个包时以空格隔开即可')
        print('|如需自动上传至fir/itc,请在每个数字后加 -a')
        print('+----------------------------+')
        print('+----------------------------+')
        selectTypes = input('请输入: ')
        rinpts = selectTypes.split(' ')
        _archive_ever_input(rinpts)
    else:
        rinpts = args[1:len(args)]
        print(rinpts[0])
        _archive_ever_input(rinpts)