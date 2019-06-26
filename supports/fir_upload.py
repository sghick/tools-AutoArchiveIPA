# coding: utf-8

####################################################################################################
# fir upload
####################################################################################################

import requests
import json
import os
import sys

split = '-' * 20

def print_split(s):
    print(split + '[ ' + s + ' ]' + split)


# 必填项，可以通过命令行参数传入

# fir 的token 和包信息
APP_INFO = {
    'api_token': 'xxx',
    'applicationId': 'bundleID',
    'versionName': 'version',
    'versionCode': 'versionCode',
    'changelog': 'log'
}


# 必填项，可以通过命令行参数传入

def init_app_info():
    if len(sys.argv) > 1:
        print_split('获取到传递过来的参数')
        print(str(sys.argv))
        APP_INFO['api_token'] = sys.argv[1]
        APP_INFO['applicationId'] = sys.argv[2]
        APP_INFO['versionName'] = sys.argv[3]
        APP_INFO['versionCode'] = sys.argv[4]
    if len(sys.argv) > 4:
        APP_INFO['changelog'] = sys.argv[5]


# 获取 fir 的上传凭证
def get_cert():
    print_split('发起获取上传凭证请求')
    data = {'type': 'ios', 'bundle_id': APP_INFO['applicationId'],
            'api_token': APP_INFO['api_token']}
    print(data)
    req = requests.post(url='http://api.fir.im/apps', data=data)
    cert_resp = req.content
    print_split('获取到 fir 响应')
    print(str(cert_resp))
    return cert_resp

# 上传到fir
def upload_fir(binary, path):
    # 拿到相应的token
    cert_key = binary['key']
    cert_token = binary['token']
    cert_upload_url = binary['upload_url']

    print_split('上传 iPA')
    file = {'file': open(path, 'rb')}
    param = {
        "key": cert_key,
        "token": cert_token,
        'x:build': APP_INFO['versionCode'],
        "x:name": '  ',
        "x:changelog": APP_INFO['changelog']
    }
    requests.packages.urllib3.disable_warnings()
    req = requests.post(cert_upload_url,files=file, data=param, verify=False)

    print(req.content)

def upload_ipa(ipa_path):
    init_app_info()
    cert_resp2 = get_cert()

    # 拿到cert实体
    cert_json = json.loads(cert_resp2)
    binary_dirt = cert_json['cert']['binary']

    upload_fir(binary_dirt, ipa_path)