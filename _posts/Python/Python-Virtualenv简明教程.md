# Python--Virtualenv简明教程

virtualenv is a tool to create isolated Python environments.
virtualenv通过创建独立Python开发环境的工具, 来解决依赖、版本以及间接权限
问题. 比如一个项目依赖Django1.3 而当前全局开发环境为Django1.7, 版本跨度过大, 导致不兼容使项目无法正在运行, 使用virtualenv可以解决这些问题.

virtualenv创建一个拥有自己安装目录的环境, 这个环境不与其他虚拟环境共享库, 能够方便的管理python版本和管理python库

- 1. 安装Virtualenv
使用pip安装Virtualenv, 使用过python的都应该知道pip包管理神器吧, 即使不知道, 网站也有大把的教程, 不过推荐查看官方安装指南

```bash
$ pip install virtualenv
//或者由于权限问题使用sudo临时提升权限
$ sudo pip install virtualenv
```

- 2. virtualenv基本使用
现在开始使用virtualenv管理python环境

```bash
$ virtualenv ENV  #创建一个名为ENV的目录, 并且安装了ENV/bin/python, 创建了lib,include,bin目录,安装了pip
New python executable in 
Installing setuptools, pip...done.

$ cd ENV
$ ll
drwxr-xr-x  14 andrew_liu  staff  476 12  8 08:49 bin
drwxr-xr-x   3 andrew_liu  staff  102 12  8 08:49 include
drwxr-xr-x   3 andrew_liu  staff  102 12  8 08:49 lib
```

lib,所有安装的python库都会放在这个目录中的lib/pythonx.x/site-packages/下
bin,bin/python是在当前环境是使用的python解释器
如果在命令行中运行virtualenv --system-site-packages ENV, 会继承/usr/lib/python2.7/site-packages下的所有库, 最新版本virtualenv把把访问全局site-packages作为默认行为
default behavior.

- - 2.1. 激活virtualenv

- - - ENV目录下使用如下命令

```bash
$ source ./bin/activate  #激活当前virtualenv
#注意终端发生了变化
```

- - - 使用pip查看当前库

```bash
$ pip list
pip (1.5.6)
setuptools (3.6)
wsgiref (0.1.2) #发现在只有这三个
pip freeze  #显示所有依赖
pip freeze > requirement.txt  #生成requirement.txt文件
pip install -r requirement.txt  #根据requirement.txt生成相同的环境
```

- - 2.2. 关闭virtualenv
使用下面命令
```bash
$ deactivate
```
- - 2.3. 指定python版本
可以使用-p PYTHON_EXE选项在创建虚拟环境的时候指定python版本


- - - 创建python2.7虚拟环境

```
$ virtualenv -p /usr/bin/python2.7 ENV2.7
Running virtualenv with interpreter /usr/bin/python2.7
New python executable in ENV2.7/bin/python
Installing setuptools, pip...done.
```

- - - 创建python3.4虚拟环境
```
$ virtualenv -p /usr/local/bin/python3.4 ENV3.4
Running virtualenv with interpreter /usr/local/bin/python3.4
Using base prefix '/Library/Frameworks/Python.framework/Versions/3.4'
New python executable in ENV3.4/bin/python3.4
Also creating executable in ENV3.4/bin/python
Installing setuptools, pip...done.
```
到此已经可以解决python版本冲突问题和python库不同版本的问题

- 3. 其他
- - 3.1. 生成可打包环境
某些特殊需求下,可能没有网络, 我们期望直接打包一个ENV, 可以解压后直接使用, 这时候可以使用virtualenv -relocatable指令将ENV修改为可更改位置的ENV

#对当前已经创建的虚拟环境更改为可迁移
```bash
$ virtualenv --relocatable ./
Making script ./bin/easy_install relative
Making script ./bin/easy_install-3.4 relative
Making script ./bin/pip relative
Making script ./bin/pip3 relative
Making script ./bin/pip3.4 relative
```

- - 3.2. 获得帮助
```bash
$ virtualenv -h
```
当前的ENV都被修改为相对路径, 可以打包当前目录, 上传到其他位置使用

这并不能使虚拟环境跨平台使用

[参考链接](http://python.jobbole.com/85398/)