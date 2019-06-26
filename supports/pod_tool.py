# coding: utf-8

import os
from conf import config
from supports import print_split

####################################################################################################
# Git, Cocoapods & xcodebuild
####################################################################################################

def git_clone_repository():
    print_split.print_log("git_clone_repository")
    respositoryDir = None
    try:
        (filepath, tempfilename) = os.path.split(config.kRepositoryGit)
        (filename, extension) = os.path.splitext(tempfilename)
        respositoryDir = config.kAutoArchiveRepositoryRootPath + filename
    except:
        print_split.print_war("未配置git仓库地址:config.kRepositoryGit")
        return

    if (not os.path.exists(respositoryDir)):
        print_split.print_war('git clone ' + config.kRepositoryGit + ' ' + respositoryDir)
        os.system('%s' % 'git clone ' + config.kRepositoryGit + ' ' + respositoryDir) 
    else:
        print_split.print_war("检查到本地git仓库已经存在")

def updateCode():
    print_split.print_log("updateCode")
    gitResetCommand = 'git reset --hard'
    gitCheckoutCommand = 'git checkout %s' % config.kBranchName
    gitBranchCommand = ''
    gitPullCommand = 'git pull'
    gitLogCommand = 'git log -1'
    os.system('%s' % config.cdCommand + ';' + gitResetCommand + ';' + gitPullCommand + ';' + gitCheckoutCommand + ';' + gitPullCommand + ';' + gitLogCommand)

def installPods():
    print_split.print_log("installPods")
    # pod install --verbose --no-repo-update
    os.system('%s' % config.cdCommand + ';' + 'pod install')

def discardAllChange():
    print_split.print_log("discardAllChange")
    os.system('%s' % config.cdCommand + ';' + 'git checkout .')

def cleanProject():
    print_split.print_log("cleanProject")
    cleanCommand = "xcodebuild -target '%s' clean" % config.kTargetName
    os.system('%s' % config.cdCommand + ';' + cleanCommand)