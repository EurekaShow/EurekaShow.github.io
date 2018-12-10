---
author: XiaoFeng
date: 2018-10-07
layout: post
title: docker搭建常用Gitlab
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - Gitlab
---
 
 # docker搭建常用Gitlab
 
```bash
 # sudo docker run --detach \
--publish 10443:443 --publish 80:80 --publish 10022:22 \
--name gitlab \
--privileged=true \
--restart always \
--volume ~/gitlab/config:/etc/gitlab \
--volume ~/gitlab/logs:/var/log/gitlab \
--volume ~/gitlab/data:/var/opt/gitlab \
gitlab/gitlab-ce:11.3.6-ce.0
```

配置外部访问URL
这个必须配置，否则默认以容器的主机名作为URL，刚开始由于做了端口映射80->8080, 因此设置为

```conf
external_url "http://10.103.240.36:8080"
```
后来发现external_url只能配置ip或者域名，不能有端口，否则不能启动。
