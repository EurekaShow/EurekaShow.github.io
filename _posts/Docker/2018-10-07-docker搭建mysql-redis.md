---
author: XiaoFeng
date: 2018-10-07
layout: post
title: docker搭建mysql
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - mysql
---

# docker搭建mysql 

```bash
## windows
# docker run --name mysql -e MYSQL_ROOT_PASSWORD=. -p 3306:3306 --privileged=true -v /d/mysql/data:/var/lib/mysql -v /d/mysql/conf:/etc/mysql -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

## linux
# docker run --name mysql -e MYSQL_ROOT_PASSWORD=. -p 3306:3306 --privileged=true -v /usr/local/data/mysql/data:/var/lib/mysql -v /usr/local/data/mysql/conf:/etc/mysql -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

## docker搭建私有仓库Mysql

- 版本 mysql5.7

```bash
#docker run --name mysql-5.7 --restart=always --privileged=true  -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d 172.16.21.239:5000/mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

解决不能远程访问的问题,正常启动不存在该问题.

```mysql
grant all privileges on *.* to root@"%" identified by "password" with grant option; 
```

## docker搭建redis
```bash
# docker run --name redis-app -p 6379:6379 --privileged=true -d redis:5-alpine
```