# coding: utf-8

####################################################################################################
# fir upload
####################################################################################################

import requests
import json
import os
import sys
from conf import config

split = '-' * 20

def print_split(s):
    print(split + '[ ' + s + ' ]' + split)


# 必填项，可以通过命令行参数传入

# fir 的token 和包信息
APP_INFO = {
    'api_token': 'xxx',
    'bundle_id': 'bundleID'
}

# 获取 fir 的上传凭证
def get_cert():
    print_split('发起获取上传凭证请求')
    data = {'type': 'ios', 'bundle_id': APP_INFO['bundle_id'],
            'api_token': APP_INFO['api_token']}
    print(data)
    req = requests.post(url='http://api.fir.im/apps', data=data)
    cert_resp = req.content
    print_split('获取到 fir 响应')
    print(str(cert_resp))
    return cert_resp

# 上传到icon到fir
def upload_icon(icon, path):
    # 拿到相应的token
    cert_key = icon['key']
    cert_token = icon['token']
    cert_upload_url = icon['upload_url']

    print_split('上传 icon')
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

    print_split('上传 iPA')
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

def upload_ipa(ipa_path, iconpath, bundle_id, netType, version, build):
    APP_INFO['api_token'] = config.fir_token
    APP_INFO['bundle_id'] = bundle_id
    changelog = ''
    if netType == 1:
        changelog = '[测试环境](自动上传)'
    else:
        changelog = '[线上环境](自动上传)'

    cert_resp2 = get_cert()
    # 拿到cert实体
    cert_json = json.loads(cert_resp2)
    binary_dirt = cert_json['cert']['binary']
    icon_dirt = cert_json['cert']['icon']
    upload_icon(icon_dirt, iconpath)
    return upload_fir(binary_dirt, ipa_path, version, build, changelog)