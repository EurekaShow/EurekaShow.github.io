---
author: XiaoFeng
date: 2018-02-07
layout: post
title: centos6安装docker
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - 容器
    - Centos6
---

# centos6安装docker

- 安装

```bash
[root@localhost ~]# yum clean all

[root@localhost ~]# yum update

[root@localhost ~]# reboot

[root@localhost ~]# rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org


[root@localhost ~]# rpm -Uvh http://www.elrepo.org/elrepo-release-6-8.el6.elrepo.noarch.rpm

[root@localhost ~]# yum --disablerepo="*" --enablerepo="elrepo-kernel" list available
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * elrepo-kernel: mirrors.neusoft.edu.cn
elrepo-kernel                                                              | 2.9 kB     00:00
elrepo-kernel/primary_db                                                   |  22 kB     00:00
Available Packages
kernel-lt.x86_64                            4.4.125-1.el6.elrepo                     elrepo-kernel
kernel-lt-devel.x86_64                      4.4.125-1.el6.elrepo                     elrepo-kernel
kernel-lt-doc.noarch                        4.4.125-1.el6.elrepo                     elrepo-kernel
kernel-lt-headers.x86_64                    4.4.125-1.el6.elrepo                     elrepo-kernel
kernel-ml.x86_64                            4.15.14-1.el6.elrepo                     elrepo-kernel
kernel-ml-devel.x86_64                      4.15.14-1.el6.elrepo                     elrepo-kernel
kernel-ml-doc.noarch                        4.15.14-1.el6.elrepo                     elrepo-kernel
kernel-ml-headers.x86_64                    4.15.14-1.el6.elrepo                     elrepo-kernel
perf.x86_64                                 4.15.14-1.el6.elrepo                     elrepo-kernel
python-perf.x86_64                          4.15.14-1.el6.elrepo                     elrepo-kernel

[root@localhost ~]# yum --enablerepo=elrepo-kernel install kernel-lt –y
```

- 修改引导文件,将默认引导改为0

```
[root@localhost ~]# uname -r
4.4.125-1.el6.elrepo.x86_64

// 如果不是最新的的,修改引导文件重启.
[root@localhost ~]# vi /etc/grub.conf

//查看新安装的内核顺序,一般是0,修改
default=0
为新安装的即可.顺序从0开始,如果不是0,修改为序号即可.

[root@localhost ~]# reboot
```

- 安装docker

安装docker可能会有无法启动的问题,建议安装docker-io

```
[root@localhost ~]# yum install docker-io
```

如果报错先安装yum源，提示:No package docker available
```

yum -y install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

yum install docker-io
```

- 修改 docker 源

docker官方的仓库在有些地方会由于莫名其妙的原因Time out,那么你可以修改成国内的源,比如要拉取网易蜂巢官方.

```bash
//Ubuntu：
[root@localhost ~]# vi /etc/default/docker
//Centos：
[root@localhost ~]# vi /etc/sysconfig/docker
//增加
 ADD_REGISTRY='--add-registry hub.c.163.com'
```

重启docker.

- 卸载docker

安装后有些版本会无法启动,可能需要卸载安装其他版本.

```bash
//查看Docker版本
[root@localhost ~]# docker version

//卸载Docker
//查看已安装的包：
[root@localhost ~]# yum list installed | grep docker

//删除软件包：
[root@localhost ~]# yum -y remove docker-io.x86_64

//删除镜像/容器：
[root@localhost ~]# rm -rf /var/lib/docker
```