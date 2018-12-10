---
author: XiaoFeng
date: 2018-02-07
layout: post
title: docker入门(七)CentOS7下使用docker-compose部署容器
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - 部署容器
    - docker-compose
---

# docker入门(七)CentOS7下使用docker-compose部署容器
知道了怎么用界面管理容器和镜像后，是不是觉得每次都docker run命令，在生产环境变化复杂和难以管理？毕竟生产环境不像测试环境，随便拉一个就Ok，那可是批量的环境阿，应用，缓存，数据库，应用集群，缓存集群，数据库集群，是不是瞬间头大了？还容易一个不小心就容易弄混，那么我们来看看，怎么高效管理docker run在生产中部署。docker 给出的方案是docker-compose，通过编辑yml文件达到统一管理容器的目的。我们先来看个示例，然后再来从安装一步步搭建一个wordpress。
```yml
version: '3.0'

services:
  webserver:
    image: wordpress
    container_name: wp_web
    ports:
      - 8080:80
    links:
      - dbserver:mysql
    environment:
      WORDPRESS_DB_PASSWORD: 6zcznAEjLWp79P
  dbserver:
    image: mysql:latest
    container_name: wp_db
    environment:
      MYSQL_ROOT_PASSWORD: 6zcznAEjLWp79P
```
多个容器一起配置，有没有觉得瞬间简单多了。
我们来从安装一步步熟悉下怎么使用：
### - 1.安装
官方给出的安装方式是：
```bash
#1
sudo curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

#2
sudo chmod +x /usr/local/bin/docker-compose

#3
$ docker-compose --version
docker-compose version 1.19.0, build 1719ceb
```
[这里有官方列出来的各个版本](https://github.com/docker/compose/releases)

官方给的安装方式虽然简单，然额，并没有太大卵用，慢的像狗屎不说，基本上都要失败。经历过几次失败后，我们要另辟蹊径了。
```bash
[root@localhost ~]# yum install epel-release -y

#安装成功的提示：
Installed:
  epel-release.noarch 0:7-9                                                                                                                           
Complete!

[root@localhost ~]# yum install python-pip -y

#我们应该看到安装成功的提示
Installed:
  python2-pip.noarch 0:8.1.2-5.el7                                                                                                       
Complete!

[root@localhost ~]# pip install docker-compose

#安装完成后，看到黄色醒目提示，如果你没有，那就可以无视了。
You are using pip version 8.1.2, however version 9.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

#根据提示更新pip
[root@localhost ~]# pip install --upgrade pip

#可以看到如下的更新成功的提示。
Collecting pip
  Downloading pip-9.0.1-py2.py3-none-any.whl (1.3MB)
    100% |████████████████████████████████| 1.3MB 343kB/s 
Installing collected packages: pip
  Found existing installation: pip 8.1.2
    Uninstalling pip-8.1.2:
      Successfully uninstalled pip-8.1.2
Successfully installed pip-9.0.1

#检验安装成功与否的标志，国际惯例，我们来看下版本。
[root@localhost ~]# docker-compose --version
docker-compose version 1.19.0, build 9e633ef
```

Ok接下来，我们要看下如何使用docker-compose搭建一个wordpress。
### - 2.搭建 wordpress 环境
```bash
[root@localhost ~]# docker pull mysql

[root@localhost ~]# docker pull wordpress

[root@localhost ~]# cd /usr/local/
[root@localhost ~]# mkdir wordpress-site
[root@localhost ~]# vim docker-compose.yml
```
在docker-compose.yml中输入
```yml
version: '2.1'

services:
  webserver:
    image: wordpress
    container_name: wp_web
    ports:
      - 8080:80
    links:
      - dbserver:mysql
    environment:
      WORDPRESS_DB_PASSWORD: 6zcznAEjLWp79P
  dbserver:
    image: mysql:latest
    container_name: wp_db
    ports:
      - 3306:3306
    environment:
      MYSQL_ROOT_PASSWORD: 6zcznAEjLWp79P
```
保存退出，在当前目录下执行：
```bash
[root@localhost ~]# docker-compose up
```

执行完成后，打开浏览器，输入http://localhost:8080看看，是否出现了熟悉而久违的wordpress安装界面。

再来回顾下docker-compose常用命令
```bash
[root@localhost wordpress]# docker-compose ps
 Name               Command               State    Ports
--------------------------------------------------------
wp_db    docker-entrypoint.sh mysqld      Exit 0        
wp_web   docker-entrypoint.sh apach ...   Exit 0   

[root@localhost wordpress]# docker-compose start
Starting dbserver  ... done
Starting webserver ... done

[root@localhost wordpress]# docker-compose ps
 Name               Command               State           Ports         
------------------------------------------------------------------------
wp_db    docker-entrypoint.sh mysqld      Up      0.0.0.0:3306->3306/tcp
wp_web   docker-entrypoint.sh apach ...   Up      0.0.0.0:8080->80/tcp  
[root@localhost wordpress]# 

```

### 补充1-yml版本和docker版本之间关系
仔细看我们开篇举例用用的yml文件和最后使用的yml的区别会发现，开篇的version有差别，这个是由于我本机安装的docker版本较低造成，这个版本决定了最终由哪个版本的docker来执行，docker和compose yml文件版本的对应关系如下：
|                     |                |
|---------------------|----------------
|Compose file format  |Docker Engine
|3.3 – 3.5	          |17.06.0+
|3.0 – 3.2	          |1.13.0+
|2.3	              |17.06.0+
|2.2	              |1.13.0+
|2.1	              |1.12.0+
|2.0	              |1.10.0+
|1.0	              |1.9.1+

因为我的yml version是2.1，那么可知我用docker版本1.12.0+。

### 补充2-不挂载外部目录的mysql容器，数据相关的文件存放在哪里？
我们知道在docker run的时候，一般情况下配置文件和数据库data目录会挂载本地的目录，如果run的时候指定了对应，那么存放位置很清楚，如果没有指定挂载本地目录，mysql文件会存放在哪里呢？请出命令来看下：
```bash
[root@localhost ~]# docker ps 
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
8f80cf5a522a        wordpress           "docker-entrypoint.sh"   2 days ago          Up 34 hours         0.0.0.0:8080->80/tcp     wp_web
4e45f5b9faea        mysql:latest        "docker-entrypoint.sh"   2 days ago          Up 34 hours         0.0.0.0:3306->3306/tcp   wp_db
[root@localhost ~]# docker inspect wp_db
[
    {
        "Id": "4e45f5b9faeada2903f30374126af51cf528a68ffecb0e3d83fc467ce6bcab0b",
        "Created": "2018-02-17T06:04:11.350344791Z",
        "Path": "docker-entrypoint.sh",
        #此处省略部分参数
        "Mounts": [
            {
                "Name": "b0f8ab549e21d519254e83d24eac6e1e1baaf22bf6939f4dd870bbb4dd7f2278",
                "Source": "/var/lib/docker/volumes/b0f8ab549e21d519254e83d24eac6e1e1baaf22bf6939f4dd870bbb4dd7f2278/_data",
                "Destination": "/var/lib/mysql",
                "Driver": "local",
                "Mode": "",
                "RW": true,
                "Propagation": ""
            }
        ]
        #省略部分参数
    }
]
#仔细看Mounts下的Source，切换到路径下我们来看下。
[root@localhost ~]# cd /var/lib/docker/volumes/b0f8ab549e21d519254e83d24eac6e1e1baaf22bf6939f4dd870bbb4dd7f2278/_data
[root@localhost _data]# ls
auto.cnf          ca-key.pem  client-cert.pem  ib_buffer_pool  ib_logfile0  ibtmp1  performance_schema  public_key.pem   server-key.pem  wordpress
beautyparlor_sys  ca.pem      client-key.pem   ibdata1         ib_logfile1  mysql   private_key.pem     server-cert.pem  sys
```
Ok，看到ibdata1就恍然大悟了，原来镜像层以外的可读写层的数据存放在这里。同理可以查看所有容器数据存放位置。
如果你加载了外部目录，那么docker inspect出来的参数里面也可以看到对应路径，挂载的目录对应在： Config->Volumes 下。


