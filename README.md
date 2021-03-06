自动打包脚本文档
=============
自动完成打包、复制ipa到服务器和发送邮件。

相关依赖
-------
1. 安装好`Xcode`
2. 安装`Python3`，可以通过[homebrew](https://brew.sh)来安装（brew install python3）

脚本介绍
-------
* 脚本共分四部分组成： 
*  - `archive.py`文件为主文件,启动脚本时,直接用`python3 archive.py`运行即可  
*  - `conf`文件夹中包含1个`config.py`配置文件,多对`xxx-Dis-ExportOptions.pllist`文件/`xxx-Dev-ExportOptions.pllist`文件,`xxx`为`targetName`
*  - `supports`文件夹中为脚本使用的辅助代码  
*  - `utils`文件夹中为脚本使用的工具类代码  

使用脚本只需要配置git地址和工程名相关的东西即可  

打包操作
-------
* 配置:  
*  - 在`config.py`文件中对要打包的工程进行配置
*  - 导出`xxx-Dev-ExportOptions.plist`和`xxx-Dis-ExportOptions.plist`文件
*  - (可以先用XCode打一次包,导出后把`ExportOptions.plist`文件复制过来,分别导出2次,一次为dev的,一次为dis的,并重命名即可)

* 执行:  
*  - cd 到脚本所在目录  
*  - 执行`python3 archive.py`  
*  - 选择打包的类型  
*  - 开始打包  

* 调试:  
*  - 导出安装包调试,可在`config.py`文件中设置`ExportOnly=Ture`:
*  - 如果`*.xcarchive`文件,将它拷贝到`__export/*/DevInner(DevOuter/AppStore)`文件夹下,可以直接进行导出测试.
	
上传fir
-------
* 需要安装requests库,使用`python3 -m pip install requests`下载

```
