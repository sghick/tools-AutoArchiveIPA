# coding: utf-8

import os
from utils import print_split
from utils import settings

####################################################################################################
# itc upload:https://help.apple.com/itc/apploader/#/apdATD1E53-D1E1A1303-D1E53A1126
####################################################################################################

def validateipa(filepath, username, password):
    print_split.print_war('ITC验证app:')
    toolcmd = '/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool'
    command = "%s --validate-app -f '%s' -u '%s' -p '%s'" % (toolcmd, filepath, username, password)
    print('altoolValidateCommand：' + command)
    os.system(command)
    return

def uploadipa(filepath, username, password):
    print_split.print_war('ITC上传app:')
    toolcmd = '/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/Frameworks/ITunesSoftwareService.framework/Versions/A/Support/altool'
    command = "%s --upload-app -f '%s' -u '%s' -p '%s'" % (toolcmd, filepath, username, password)
    print('altoolUploadCommand：' + command)
    os.system(command)
    return

def uploaditc(filepath, username, password):
    validateipa(filepath, username, password)
    uploadipa(filepath, username, password)
    return



    