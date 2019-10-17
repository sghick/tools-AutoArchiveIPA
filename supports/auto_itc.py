# coding: utf-8

import os
from utils import print_split
from utils import settings

####################################################################################################
# itc upload:https://help.apple.com/itc/apploader/#/apdATD1E53-D1E1A1303-D1E53A1126
####################################################################################################

def validateipa(filepath, username, password):
    print_split.print_war('ITC验证app:')
    toolcmd = 'xcrun altool'
    command = "%s --validate-app -f '%s' -t ios -p '%s' -u '%s'" % (toolcmd, filepath, password, username)
    print('altoolValidateCommand：' + command)
    os.system(command)
    return

def uploadipa(filepath, username, password):
    print_split.print_war('ITC上传app:')
    toolcmd = 'xcrun altool'
    command = "%s --upload-app -f '%s' -t ios -p '%s' -u '%s'" % (toolcmd, filepath, password, username)
    print('altoolUploadCommand：' + command)
    os.system(command)
    return

def uploaditc(filepath, username, password):
    validateipa(filepath, username, password)
    uploadipa(filepath, username, password)
    return



    
