#docker入门
讲解docker架构/理论/概念的文章比较多，本系列只做实操练习，如果您对理论和概念比较关注，在本文结尾会推荐相关文章。

- 1.安装
```bash
[root@localhost ~]# yum install docker
```

- 2.启动服务
```bash
[root@localhost ~]# service docker start 
#centos 7 下，也可以执行
[root@localhost ~]# systemctl start  docker

#设置为开机启动
[root@localhost ~]# chkconfig docker on
#centos 7 下，可以执行一下命令
[root@localhost ~]# systemctl enable docker
```

- 3.查询docker hub上现有的镜像文件并使用
```bash
#设置为开机启动
[root@localhost ~]# docker search helloword

#拉取想要的镜像
[root@localhost ~]# docker pull helloword（镜像完整名称或者id，名称需要是查询出来的带/的所有字符）
```

- 4.启动镜像
```bash
[root@localhost ~]# docker run -it --name my_helloworld -p 80:8080 helloworld /bin/bash
```

至此，一套docker入门拳就打通了，一哈哈。

- 来熟悉下常用操作命令
```bash
#查询docker hub上的镜像文件
docker search 关键字

#拉取指定镜像
docker pull 镜像名称（需要完整的名称）

#根据镜像生成容器
docker run --privileged --cap-add SYS_ADMIN -e container=docker -it --name my_tomcat -p 0.0.0.0:8080:8080  -d  --restart=always tomcat
docker run -it --name tomcat -p 80:8080 java8-tomcat8 /bin/bash

#启动镜像
docker start 容器名称（在上一步中生成的容器名称为my_tomcat）

#进入正在运行的镜像
docker exec -it 镜像名称 /bin/bash

#查看镜像内部的linux版本
cat /etc/*-release

#更新镜像文件，更新后，可以对镜像文件进行修改
apt-get update

#把修改后的容器生成新的镜像
docker commit 容器ID 新镜像名称   
```
这里有篇更详细的描述可供参考，包含了docker旧版本的删除等操作。
[centos安装docker容器](http://www.cnblogs.com/coolworld/p/5486640.html)

这篇文章可以帮你入门基础概念
[Docker基础之一: Docker架构](https://yq.aliyun.com/articles/130)