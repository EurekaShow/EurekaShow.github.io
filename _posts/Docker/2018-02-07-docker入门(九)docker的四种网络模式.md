---
author: XiaoFeng
date: 2018-02-07
layout: post
title: docker入门(九)docker的四种网络模式
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - 网络模式
---

# docker入门(九)docker的四种网络模式

### Docker的四种网络模式(host、container、none、bridge)

- 1、 host模式，使用docker run时使用--net=host指定，docker使用的网络实际上和宿主机一样，在容器内看到的网卡ip是宿主机上的ip
```bash
   # docker run -it --rm --net=host httpd bash
```
- 2、container模式，使用--net=container:container_id/container_name多个容器使用共同的网络，看到的ip是一样的

- 3、none模式，使用--net=none指定：这种模式下不会配置任何网络

- 4、bridge模式，使用--net=bridge指定，默认模式，不用指定，默认就是这种模式，这种模式会为每个容器分配一个独立的Network Namespace。类似于vmware的nat网络模式，同一个宿主机上的所有容器会在同一个网段下，相互之间可以通信
