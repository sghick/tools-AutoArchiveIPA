# coding: utf-8

import os
from utils import print_split
from utils import settings

####################################################################################################
# Git, Cocoapods & xcodebuild
####################################################################################################

def git_clone_repository(repositoryGit):
    print_split.print_log("gitCloneRepository")
    respositoryDir = None
    try:
        (filepath, tempfilename) = os.path.split(repositoryGit)
        (filename, extension) = os.path.splitext(tempfilename)
        respositoryDir = settings.kAutoArchiveRepositoryRootPath + filename
    except:
        print_split.print_war("未配置git仓库地址")
        return

    if (not os.path.exists(respositoryDir)):
        print_split.print_war('git clone ' + repositoryGit + ' ' + respositoryDir)
        os.system('%s' % 'git clone ' + repositoryGit + ' ' + respositoryDir) 
    else:
        print_split.print_war("检查到本地git仓库已经存在")

def updateCode(repositoryName, branchName):
    print_split.print_log("updateCode")
    gitResetCommand = 'git reset --hard'
    gitCheckoutCommand = 'git checkout %s' % branchName
    gitBranchCommand = ''
    gitPullCommand = 'git pull'
    gitLogCommand = 'git log -1'
    os.system('%s' % settings.cmd_cd(repositoryName) + ';' + gitResetCommand + ';' + gitPullCommand + ';' + gitCheckoutCommand + ';' + gitPullCommand + ';' + gitLogCommand)

def installPods(repositoryName):
    print_split.print_log("installPods")
    # pod install --verbose --no-repo-update
    os.system('%s' % settings.cmd_cd(repositoryName) + ';' + 'pod install')

def discardAllChange(repositoryName):
    print_split.print_log("discardAllChange")
    os.system('%s' % settings.cmd_cd(repositoryName) + ';' + 'git checkout .')

def cleanProject(repositoryName, targetName):
    print_split.print_log("cleanProject")
    cleanCommand = "xcodebuild -target '%s' clean" % targetName
    os.system('%s' % settings.cmd_cd(repositoryName) + ';' + cleanCommand)