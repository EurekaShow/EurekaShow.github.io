# docker入门(三)制作自己的镜像文件

熟悉了常用的操作，可以pull别人的镜像之后，忍不住要做自己镜像啦。
自己做镜像分2部分：

- 1.根据需要创建自己的Dockerfile。
- 2.把创建Dockfile脚本文件以Dockerfile命名。

我们将要创建一个包含Java8，Tomcat8的CentOS镜像。
let's go！

## - 1.创建脚本，脚本内容如下：

```bash
#基础镜像
FROM centos

#维护人员信息
MAINTAINER eureka "euka.news@163.com"

#设置工作目录，这个命令是用来切换工作目录的，相当于cd命令
WORKDIR /usr/local

#安装JDK
#创建JDK目录，等一下的JDK安装到这个目录
RUN mkdir java

#上篇文章中已经下载了jdk，为了节省时间我这里使用COPY命令将宿主机中的jdk压缩包复制到镜像中，这样做存在的问题是使用Dockerfile创建镜像的宿主机必须在对应的路
#径下有这个包。我这里的包和Dockerfile文件在同一个目录下，源文件的路径需要是Dockerfile文件所在目录(上下文根目录)的相对路径
#也可以使用wget、 apt-get等命令在线下载
COPY jdk-8u162-linux-x64.tar.gz /usr/local/

#解压复制到镜像中的jdk压缩包，完成后删除，RUN命令可以使用 && 将两条命令放到一起，减少镜像的层数
RUN tar zxf /usr/local/jdk-8u162-linux-x64.tar.gz -C /usr/local/java && rm -rf /usr/local/jdk-8u162-linux-x64.tar.gz

#设置环境变量
ENV JAVA_HOME /usr/local/java/jdk1.8.0_162
ENV PATH $PATH:$JAVA_HOME/bin

#安装tomcat，同JDK
RUN mkdir tomcat 
COPY apache-tomcat-8.0.49.tar.gz /usr/local/
RUN tar zxf /usr/local/apache-tomcat-8.0.49.tar.gz -C /usr/local/tomcat && rm -rf /usr/local/apache-tomcat-8.0.49.tar.gz

#暴露tomcat的内部端口，如果没有修改tomcat的配置文件的话，默认是8080端口
EXPOSE 8080

#启动容器时，执行脚本文件启动Tomcat并持续输出日志，防止容器退出。
ENTRYPOINT /usr/local/tomcat/apache-tomcat-8.0.49/bin/startup.sh && tail -f /usr/local/tomcat/apache-tomcat-8.0.49/logs/catalina.out
```

## - 2.然后把脚本文件命名为Dockerfile，把下载好的JDK和Tomcat拷贝到相同路径。

## - 3.执行build命令：

```bash
#因为Dockerfile和安装包我都拷贝到了Downloads目录，所以build路径是.
[root@localhost Downloads]# docker build -t java8-tomcat8 .
Sending build context to Docker daemon 950.5 MB
Step 1 : FROM centos
 ---> ff426288ea90
Step 2 : MAINTAINER eureka "euka.news@163.com"
 ---> Running in 00de8fe813f7
 ---> 3ea338519916
Removing intermediate container 00de8fe813f7
Step 3 : WORKDIR /usr/local
 ---> Running in 37710ef45ef8
 ---> 3f22d4e7042f
Removing intermediate container 37710ef45ef8
Step 4 : RUN mkdir java
 ---> Running in 51bf73519b69
 ---> 0c37ed65a0fa
Removing intermediate container 51bf73519b69
Step 5 : COPY jdk-8u162-linux-x64.tar.gz /usr/local/
 ---> 974d66a31c1d
Removing intermediate container d5ef03fee0c0
Step 6 : RUN tar zxf /usr/local/jdk-8u162-linux-x64.tar.gz -C /usr/local/java && rm -rf /usr/local/jdk-8u162-linux-x64.tar.gz
 ---> Running in b0c660a70e51
 ---> d864ea0e87cf
Removing intermediate container b0c660a70e51
Step 7 : ENV JAVA_HOME /usr/local/java/jdk1.8.0_162
 ---> Running in d844ce7710db
 ---> b2ce57ac07fb
Removing intermediate container d844ce7710db
Step 8 : ENV PATH $PATH:$JAVA_HOME/bin
 ---> Running in 2233858bbdfc
 ---> e96cd1c09b87
Removing intermediate container 2233858bbdfc
Step 9 : RUN mkdir tomcat
 ---> Running in 9496d4751db3
 ---> 2910eb802db7
Removing intermediate container 9496d4751db3
Step 10 : COPY apache-tomcat-8.0.49.tar.gz /usr/local/
 ---> 365237b7d9f6
Removing intermediate container 4624c2e20150
Step 11 : RUN tar zxf /usr/local/apache-tomcat-8.0.49.tar.gz -C /usr/local/tomcat && rm -rf /usr/local/apache-tomcat-8.0.49.tar.gz
 ---> Running in 5251cf4e158e
 ---> 1b683f639d90
Removing intermediate container 5251cf4e158e
Step 12 : EXPOSE 8080
 ---> Running in cac45fa14af6
 ---> ab668ef9fc92
Removing intermediate container cac45fa14af6
Step 13 : ENTRYPOINT /usr/local/tomcat/apache-tomcat-8.0.49/bin/startup.sh && tail -f /usr/local/tomcat/apache-tomcat-8.0.49/logs/catalina.out
 ---> Running in 2fbc4c130243
 ---> 1b8dc93ddae5
Removing intermediate container 2fbc4c130243
Successfully built 1b8dc93ddae5
```

看到Successfully真开心阿。

## - 4.查看下刚刚创建成功的镜像文件

```bash
[root@localhost Downloads]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
java8-tomcat8       latest              1b8dc93ddae5        24 minutes ago      804.5 MB
docker.io/centos    latest              ff426288ea90        4 weeks ago         207.2 MB
```
可以看到，除了我们创建的镜像文件，还有一个docker.io/centos，因为我们是给予centos创建的，所以build脚本自动会拉去官方的基础镜像文件，然后合成我们最终需要的。

## - 5.接下来，我们run下看看效果啦

```bash
[root@localhost Downloads]# docker run -it --name tomcat --link mysql:mysql --privileged=true -p 80:8080 java8-tomcat8 /bin/bash
Using CATALINA_BASE:   /usr/local/tomcat/apache-tomcat-8.0.49
Using CATALINA_HOME:   /usr/local/tomcat/apache-tomcat-8.0.49
Using CATALINA_TMPDIR: /usr/local/tomcat/apache-tomcat-8.0.49/temp
Using JRE_HOME:        /usr/local/java/jdk1.8.0_162
Using CLASSPATH:       /usr/local/tomcat/apache-tomcat-8.0.49/bin/bootstrap.jar:/usr/local/tomcat/apache-tomcat-8.0.49/bin/tomcat-juli.jar
Tomcat started.
#省略若干加载日志输出
12-Feb-2018 07:04:15.582 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
12-Feb-2018 07:04:15.605 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-nio-8009"]
12-Feb-2018 07:04:15.611 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 2426 ms
```

看到启动完成的输出，开心吧

## - 6.接着我们要做的是看看到底能不能访问啦

打开浏览器，输入http://localhost,可以看到久违的tomcat界面啦。

## - 7.那么，我们来看看现在是什么样的。

```bash
[root@localhost Downloads]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                            PORTS               NAMES
a784e5677e94        java8-tomcat8       "/bin/sh -c '/usr/loc"   5 minutes ago       Exited (130) About a minute ago                       tomcat

#停止看看，是不是不能访问啦？
[root@localhost Downloads]# docker stop a784e5677e94
a784e5677e94

#Ok，以后再用，不需要run命令了，因为我们已经创建好了容器，只需要start就好了。
[root@localhost Downloads]# docker start a784e5677e94
a784e5677e94

```

再访问http://localhost看看，完美啦。
是不是禁不住好奇想看看内部是什么样子的？

## - 8.进入容器，查看容器内部的模样

```bash

#执行docker exec后，注意看路径，如果进入成功，路径会变成容器ID哒。
[root@localhost Downloads]# docker exec -it a784e5677e94 /bin/bash
[root@a784e5677e94 local]# ls
bin  etc  games  include  java  lib  lib64  libexec  sbin  share  src  tomcat

#如果你要把文件拷贝的容器里，格式为：
# docker cp 本地文件名（含路径） 容器id/name:容器内文件名（含完整路径）
[root@a784e5677e94 local]# docker cp ./website.war tomcat:/usr/local/tomcat/webapps/website.war

```

也就是说，你可以接着做修改哟，到此位置，降龙十八掌，打完收工。

## - 9.最后的小花絮，当你对制作自己的镜像文件上瘾后，你一定希望自己有一仓库的各种各样的Dockerfile吧？

这里能满足你这美妙的梦想，有Dockerfile，有Docker images，还有很多相同乐趣的人，请移步这里看看哟：
[docker hub](https://hub.docker.com)
比如：
- [mysql](https://hub.docker.com/r/library/mysql/)
- [rabbitmq](https://hub.docker.com/_/rabbitmq/)
- [java](https://hub.docker.com/_/java/)
- [elasticsearch](https://hub.docker.com/_/elasticsearch/)
- [iis](https://hub.docker.com/r/microsoft/iis/)
- [redis](https://hub.docker.com/_/redis/)
- [nginx](https://hub.docker.com/_/nginx/)
- [mongodb](https://hub.docker.com/_/mongo/)