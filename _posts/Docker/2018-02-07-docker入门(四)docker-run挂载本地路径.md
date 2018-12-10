---
author: XiaoFeng
date: 2018-02-07
layout: post
title: docker入门(四)docker run挂载本地路径
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - 容器
    - 挂载本地路径
---

# docker入门(四)docker run挂载本地路径

### - 1.先看上次我们最后run的脚本
```bash
[root@localhost Downloads]# docker run -it --name tomcat -p 80:8080 java8-tomcat8 /bin/bash
```

### - 2.我想把日志记录到宿主机上，这样所有的容器的输出统一管理在某个指定目录，run增加 -v参数，挂载本地路径
```bash
[root@localhost Downloads]# docker run -it --name tomcat_clog -p 8080:8080 -v /usr/tmp/logs:/usr/local/tomcat/apache-tomcat-8.0.49/logs java8-tomcat8 /bin/bash
Using CATALINA_BASE:   /usr/local/tomcat/apache-tomcat-8.0.49
Using CATALINA_HOME:   /usr/local/tomcat/apache-tomcat-8.0.49
Using CATALINA_TMPDIR: /usr/local/tomcat/apache-tomcat-8.0.49/temp
Using JRE_HOME:        /usr/local/java/jdk1.8.0_162
Using CLASSPATH:       /usr/local/tomcat/apache-tomcat-8.0.49/bin/bootstrap.jar:/usr/local/tomcat/apache-tomcat-8.0.49/bin/tomcat-juli.jar
touch: cannot touch '/usr/local/tomcat/apache-tomcat-8.0.49/logs/catalina.out': Permission denied
/usr/local/tomcat/apache-tomcat-8.0.49/bin/catalina.sh: line 456: /usr/local/tomcat/apache-tomcat-8.0.49/logs/catalina.out: Permission denied
```

问题来了，Permission denied很明显是容器读取宿主机路径权限问题。
问题原因及解决办法
原因是CentOS7中的安全模块selinux把权限禁掉了，至少有以下三种方式解决挂载的目录没有权限的问题：
- 1.在运行容器的时候，给容器加特权，及加上 --privileged=true 参数：
docker run -i -t -v /soft:/soft --privileged=true 686672a1d0cc /bin/bash
- 2.临时关闭selinux：
setenforce 0
- 3.添加selinux规则，改变要挂载的目录的安全性文本

```bash
[root@localhost Downloads]# docker run -it --name tomcat_clog -p 8080:8080 -v /usr/tmp/logs:/usr/local/tomcat/apache-tomcat-8.0.49/logs --privileged=true java8-tomcat8 /bin/bash

Using CATALINA_BASE:   /usr/local/tomcat/apache-tomcat-8.0.49
Using CATALINA_HOME:   /usr/local/tomcat/apache-tomcat-8.0.49
Using CATALINA_TMPDIR: /usr/local/tomcat/apache-tomcat-8.0.49/temp
Using JRE_HOME:        /usr/local/java/jdk1.8.0_162
Using CLASSPATH:       /usr/local/tomcat/apache-tomcat-8.0.49/bin/bootstrap.jar:/usr/local/tomcat/apache-tomcat-8.0.49/bin/tomcat-juli.jar
Tomcat started.
#此处省略若干启动加载日志
12-Feb-2018 08:31:55.653 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
12-Feb-2018 08:31:55.768 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-nio-8009"]
12-Feb-2018 08:31:55.772 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 3334 ms
```
到宿主机制定路径下，能看到tomcat生成的对应log文件。说明挂载本地目录成功。

### - 3.我还想把项目部署到本地，当然可以的呀,多个目录挂载嘛
```bash
[root@localhost Downloads]# docker run -it --name tomcat_db_path -p 8081:8080 -v /usr/tmp/logs2:/usr/local/tomcat/apache-tomcat-8.0.49/logs2 -v /usr/tmp/webapps:/usr/local/tomcat/apache-tomcat-8.0.49/webapps --privileged=true java8-tomcat8 /bin/bash
```
这么直接映射完肯定tomcat启动页都看不到，为了用tomcat启动页验证我们的杰出成果，我们来把之前的容器里面的东西拷贝到我们挂载的本地目录下
```bash
[root@localhost Downloads]# docker cp a784e5677e94:/usr/local/tomcat/apache-tomcat-8.0.49/webapps /usr/tmp/
```
Ou啦，输入http://locahost:8081看看，是不是那熟悉的tomcat启动页又回来了。
### - 4.还想映射多个端口？这都不是事儿
```bash
[root@localhost Downloads]# docker run -it --name tomcat_db_path -p 8081:8080 -p 8082:8090 -v /usr/tmp/logs2:/usr/local/tomcat/apache-tomcat-8.0.49/logs2 -v /usr/tmp/webapps:/usr/local/tomcat/apache-tomcat-8.0.49/webapps --privileged=true java8-tomcat8 /bin/bash
```

## 累了，run脚本写够了，那么来试试docker-compose吧。