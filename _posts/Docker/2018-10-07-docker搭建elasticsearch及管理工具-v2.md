---
author: XiaoFeng
date: 2018-10-07
layout: post
title: docker搭建elasticsearch及管理工具
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - elasticsearch
    - elasticsearch-head
---

# docker搭建elasticsearch及管理工具

- 搭建
  
```bash
## 创建第一台服务
# docker run -d -p 9500:9200 -p 9501:9300 --name es1 -h es1\
 -e cluster.name=ek-es -e ES_JAVA_OPTS="-Xms512m -Xmx512m" -e xpack.security.enabled=false\
  elasticsearch:2.4-alpine

## 安装elasticsearch-head
##2.0之前的版本
# /bin/plugin -install mobz/elasticsearch-head
## 2.0以后的版本
# bin/plugin install mobz/elasticsearch-head
## 5.0之后的版本该插件无法安装独立成一个服务

## 集群，该节点设置了暂时无效，有待后续查找原因
#  docker run -d -p 9505:9200 -p 9506:9300 --link es1\
  --name es2 -e cluster.name=ek-es -e xpack.security.enabled=false\
  -e ES_JAVA_OPTS="-Xms512m -Xmx512m" -e discovery.zen.ping.unicast.hosts=es1 elasticsearch:2.4-alpine

## 如果需要分析和统计图表，请使用
#  docker run -d --name kibana  --link es1 -e ELASTICSEARCH_URL=http://es1:9200 -p 5601:5601 kibana:5.6

```

- 健康检查
  
```bash
# curl -XGET http://127.0.0.1:9200/_cluster/health?pretty
```

- head插件访问
  
```bash
http://{你的ip地址}:9200/_plugin/head/
```

- 安全问题（严重）。
因为head插件可以对数据进行，增删改查。故生产环境尽量不要使用，如果要使用，最少要限制IP地址。尽量不要使用。