# CentOS常用命令

## 安装使用vim
### 1.安装
```
yum -y install vim-enhanced
#或者
yum -y install vim*
```

##CentOS 6.5配置防火墙开启指定端口
### 1.配置
```
#直接关闭防火墙
/etc/init.d/iptables stop
#或者 指定端口
/sbin/iptables -I INPUT -p tcp --dport 8080 -j ACCEPT #8080
#将更改进行保存
/etc/rc.d/init.d/iptables save 
#重启防火墙以便改动生效
/etc/init.d/iptables restart 
```

## 文件/文件夹操作
```
#创建java目录
mkdir /usr/local/java

#移动整个目录到目标目录下
mv /usr/tmp/java /usr/local/

#或者这样
mv /usr/tmp/java/ /usr/local/java

#复制文件/文件夹到指定目录
cp -R /usr/tmp/java/ /usr/local/java

#复制文件/文件夹到指定目录
cp -R /usr/tmp/java/ /usr/local/java

#创建文件file1.php的带着符号 ‘~’的备份文件file2.php~
cp -b file1.php file2.php

#直接删除java目录，不提示
rm -rf /usr/local/java

#删除java目录。
#递归的删除参数表中的目录及其子目录。 目录将被清空并且删除。 当删除目录包含的具有写保护的文件时用户通常是被提示的。
rm -r /usr/local/java
```

## zip unzip命令
### 1.安装
```
yum install zip unzip 
```
### 2.使用
```
#压缩当前目录下的data目录内容为data.zip文件
zip -r data.zip data

#解压当前目录下的data.zip文件到到data目录
unzip data.zip -d data 
```

## tar 命令
### 1.参数说明
-c ：建立一个压缩文件的参数指令(create 的意思)； 
-x ：解开一个压缩文件的参数指令！ 
-t ：查看 tarfile 里面的文件！

特别注意，在参数的下达中， c/x/t 仅能存在一个！不可同时存在！ 因为不可能同时压缩与解压缩。 
-z ：是否同时具有 gzip 的属性？亦即是否需要用 gzip 压缩？ 
-j ：是否同时具有 bzip2 的属性？亦即是否需要用 bzip2 压缩？ 
-v ：压缩的过程中显示文件！这个常用，但不建议用在背景执行过程！ 
-f ：使用档名，请留意，在 f 之后要立即接档名喔！不要再加参数！

例如使用『 tar -zcvfP tfile sfile』就是错误的写法，要写成『 tar -zcvPf tfile sfile』 
-p ：使用原文件的原来属性（属性不会依据使用者而变） 
-P ：可以使用绝对路径来压缩！ 
-N ：比后面接的日期(yyyy/mm/dd)还要新的才会被打包进新建的文件中！ 
--exclude FILE：在压缩的过程中，不要将 FILE 打包！
### 2.使用示例 
```
#打包/压缩文件夹
[root@localhost ~]# tar -cvf /tmp/etc.tar /etc      　　　　<==仅打包，不压缩！ 
[root@localhost ~]# tar -zcvf /tmp/etc.tar.gz /etc  　　　　<==打包后，以 gzip 压缩 
[root@localhost ~]# tar -jcvf /tmp/etc.tar.bz2 /etc　　　　 <==打包后，以 bzip2 压缩 

# 在预设的情况下，我们可以将压缩档在任何地方解开的！以下范例来说， 
# 我先将工作目录变换到 /usr/local/src 底下，并且解开 /tmp/etc.tar.gz ， 
# 则解开的目录会在 /usr/local/src/etc 呢！另外，如果您进入 /usr/local/src/etc 
# 则会发现，该目录下的文件属性与 /etc/ 可能会有所不同喔！
[root@localhost ~]# cd /usr/local/src 
[root@localhost src]# tar -zxvf /tmp/etc.tar.gz 

#将 /etc/ 内的所有文件备份下来，并且保存其权限！
# 这个 -p 的属性是很重要的，尤其是当您要保留原本文件的属性时！
[root@localhost ~]# tar -zxvpf /tmp/etc.tar.gz /etc

#在 /home 当中，比 2012/09/11 新的文件才备份
[root@localhost ~]# tar -N "2012/09/11" -zcvf home.tar.gz /home 
```