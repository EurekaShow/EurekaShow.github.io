---
author: XiaoFeng
date: 2018-02-07
layout: post
title: docker入门(十)docker集中化web界面管理平台-Shipyard(草稿)
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - Shipyard
    - 管理工具
---

# docker入门(十)docker集中化web界面管理平台-Shipyard(草稿)
还记得前面讲过的DockerUI么？虽然好用，可惜是单机版，对于多服务器部署的docker来说，那就是鸡肋阿。有句话怎么讲的？别不把鸡肋当鸡肉，那么，今天我们要给自己加一个大鸡腿，一起来看看shipyard。
官方给出来的安装部署方式：
```bash
[root@localhost usr]# docker run --rm --privileged=true -v /var/run/docker.sock:/var/run/docker.sock shipyard/deploy start
Pulling image: shipyard/rethinkdb
Starting Rethinkdb Data
Starting Rethinkdb
Starting Shipyard
Pulling image: shipyard/shipyard:latest
Shipyard Stack started successfully
 Username: admin Password: shipyard
[root@localhost usr]# docker ps -a
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS                         PORTS                                                                         NAMES
6c80b2a1c792        shipyard/shipyard:latest   "/bin/controller"        11 seconds ago      Restarting (0) 1 seconds ago   0.0.0.0:8080->8080/tcp                                                        shipyard
ca8f59c97657        shipyard/rethinkdb         "/usr/bin/rethinkdb -"   16 seconds ago      Up 15 seconds                  0.0.0.0:32773->8080/tcp, 0.0.0.0:32772->28015/tcp, 0.0.0.0:32771->29015/tcp   shipyard-rethinkdb
f9681bad1ba8        shipyard/rethinkdb         "/bin/bash -l"           16 seconds ago      Up 15 seconds                  8080/tcp, 28015/tcp, 29015/tcp                                                shipyard-rethinkdb-data
```
***然额，shipyard容器的状态提示总是Restarting seconds ago。***

### sec2
##### 管理服务器安装启动容器如下
docker run -ti -d --restart=always --privileged=true --name shipyard-rethinkdb rethinkdb
docker run -ti -d -p 54001:4001 -p 57001:7001 --restart=always --privileged=true --name shipyard-discovery  microbox/etcd -name discovery
docker run -ti -d -p 2375:2375 --hostname=192.168.70.135 --restart=always --privileged=true --name shipyard-proxy -v /var/run/docker.sock:/var/run/docker.sock -e PORT=2375 shipyard/docker-proxy:latest
docker run -ti -d --restart=always --privileged=true --name shipyard-swarm-manager swarm:latest manage --host tcp://0.0.0.0:3375 etcd://192.168.70.135:54001
docker run -ti -d --restart=always --privileged=true --name shipyard-swarm-agent swarm:latest join --addr 192.168.70.135:2375 etcd://192.168.70.135:54001
docker run -ti -d --restart=always --privileged=true --name shipyard-controller --link shipyard-rethinkdb:rethinkdb --link shipyard-swarm-manager:swarm  -p 58081:8080 shipyard/shipyard:latest server -d tcp://swarm:3375
##### 127服务器，shipyard有两个节点 一个是自己本身，一个是127
docker run -ti -d -p 2375:2375 --hostname=192.168.220.127 --restart=always --privileged=true --name shipyard-proxy -v /var/run/docker.sock:/var/run/docker.sock -e PORT=2375 shipyard/docker-proxy:latest
docker run -ti -d --restart=always --privileged=true --name shipyard-swarm-agent swarm:latest join --addr 192.168.220.127:2375 etcd://192.168.70.135:54001

***使用该方法部署后，登陆一切正常，却无法获取容器和镜像***

相关内容
[maxwhale/shipyard-Chinese](https://github.com/maxwhale/shipyard-Chinese)