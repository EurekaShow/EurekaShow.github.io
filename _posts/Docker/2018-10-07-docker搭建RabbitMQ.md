---
author: XiaoFeng
date: 2018-10-07
layout: post
title: docker搭建RabbitMQ
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - RabbitMQ
---

# docker搭建RabbitMQ

- 版本:rabbitmq:3-management
- 介绍:基于rabbitMQ 3.7.4版本,包含管理插件

```bash
# docker run -d --hostname rabbit-server --name rabbitMQ3 --restart=always -e RABBITMQ_DEFAULT_USER=ankangtong -e RABBITMQ_DEFAULT_PASS=ankangtong -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```