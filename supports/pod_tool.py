# coding: utf-8

import os
from conf import config

####################################################################################################
# Git, Cocoapods & xcodebuild
####################################################################################################

def git_clone_repository():
    print('=== git_clone_repository ===')
    respositoryDir = None
    try:
        (filepath, tempfilename) = os.path.split(config.kRepositoryGit)
        (filename, extension) = os.path.splitext(tempfilename)
        respositoryDir = config.kAutoArchiveRepositoryRootPath + filename
    except:
        print('未配置git仓库地址:config.kRepositoryGit')
        return

    if (not os.path.exists(respositoryDir)):
        print('git clone ' + config.kRepositoryGit + ' ' + respositoryDir)
        os.system('%s' % 'git clone ' + config.kRepositoryGit + ' ' + respositoryDir) 
    else:
        print('检查到本地git仓库已经存在')     

def updateCode():
    print('=== updateCode ===')
    gitResetCommand = 'git reset --hard'
    gitCheckoutCommand = 'git checkout %s' % config.kBranchName
    gitBranchCommand = ''
    gitPullCommand = 'git pull'
    gitLogCommand = 'git log -1'
    os.system('%s' % config.cdCommand + ';' + gitResetCommand + ';' + gitPullCommand + ';' + gitCheckoutCommand + ';' + gitPullCommand + ';' + gitLogCommand)

def installPods():
    print('=== installPods ===')
    # pod install --verbose --no-repo-update
    os.system('%s' % config.cdCommand + ';' + 'pod install')

def discardAllChange():
    print('=== discardAllChange ===')
    os.system('%s' % config.cdCommand + ';' + 'git checkout .')

def cleanProject():
    print('=== cleanProject ===')
    cleanCommand = "xcodebuild -target '%s' clean" % config.kTargetName
    os.system('%s' % config.cdCommand + ';' + cleanCommand)