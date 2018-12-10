---
author: XiaoFeng
date: 2018-02-07
layout: post
title: docker入门(八)docker-compose的YML语法之links
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - docker-compose
    - YML
    - links
---

# docker入门(八)docker-compose的YML语法之links
之所以想单独说说links，问题在于它和docker run中的link很像，但是使用上又有些区别是需要注意的，首先来看看docker run中的link怎么使用

### link
```bash
[root@localhost ~]# docker run --link 容器名称:容器别名
```

### links
链接到另一个服务中的容器。请指定服务名称和链接别名（SERVICE：ALIAS），或仅指定服务名称。
```yml
web:
  links:
   - db
   - db:database
   - redis
```
如果未指定别名，则可以在与别名相同的主机名或服务名称处访问链接服务的容器。
链接也以与depends_on相同的方式表示服务之间的依赖关系，因此它们确定服务启动的顺序。
注意：如果您定义链接和networks，则具有它们之间的链接的服务必须共享至少一个公共网络以便进行

使用的别名将会自动在服务容器中的 /etc/hosts 里创建。例如：
```
172.17.2.186  db
172.17.2.186  database
172.17.2.187  redis
```
相应的环境变量也将被创建。

在YML中，links指定的是服务名称，何为服务名称？仔细看，web极为服务名称，为了便于说明问题，我们把前面用到的YML文件拿过来对比下：
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
在这个模版文件中，webserver和dbserver即为服务名称，而不是container_name，但是在docker run的link中，指定的恰恰是这里的container_name。

更多关于模版文件这里有详细的说明

[如何写docker-compose.yml，Docker compose file 参考文档](https://deepzz.com/post/docker-compose-file.html)

[YAML 模板文件](http://wiki.jikexueyuan.com/project/docker-technology-and-combat/yaml_file.html)

刨根问底的话，这里有篇讲docker参数的文章。

[Understanding Docker Build Args, Environment Variables and Docker Compose Variables](https://vsupalov.com/docker-env-vars/)
