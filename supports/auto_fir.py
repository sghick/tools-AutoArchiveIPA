# coding: utf-8

####################################################################################################
# fir upload
####################################################################################################

import requests
import json
import os
import sys
from utils import print_split

# 获取 fir 的上传凭证
def get_cert(bundle_id, api_token):
    print_split.print_log('发起获取上传凭证请求')
    data = {'type': 'ios', 'bundle_id': bundle_id,
            'api_token': api_token}
    print(data)
    req = requests.post(url='http://api.bq04.com/apps', data=data)
    cert_resp = req.content
    print_split.print_log('获取到 fir 响应')
    print(str(cert_resp))
    return cert_resp

# 上传到icon到fir
def upload_icon(icon, path):
    # 拿到相应的token
    cert_key = icon['key']
    cert_token = icon['token']
    cert_upload_url = icon['upload_url']

    print_split.print_log('上传 icon')
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

    print_split.print_log('上传 iPA')
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

def upload_ipa(fir_token, ipa_path, iconpath, bundle_id, netType, version, build):
    changelog = ''
    if netType == 1:
        changelog = '[测试环境](脚本自动上传,请添加更新说明)'
    else:
        changelog = '[线上环境](脚本自动上传,请添加更新说明)'

    cert_resp2 = get_cert(bundle_id, fir_token)
    # 拿到cert实体
    cert_json = json.loads(cert_resp2)
    binary_dirt = cert_json['cert']['binary']
    icon_dirt = cert_json['cert']['icon']
    downloadurl = 'https://fir.im/' + cert_json['short']
    operalurl = 'https://fir.im/apps/' + cert_json['id']
    upload_icon(icon_dirt, iconpath)
    upload_fir(binary_dirt, ipa_path, version, build, changelog)
    return downloadurl, operalurl