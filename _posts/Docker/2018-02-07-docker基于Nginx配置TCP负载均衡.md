---
author: XiaoFeng
date: 2018-02-07
layout: post
title: docker基于Nginx配置TCP负载均衡
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - Nginx
    - TCP
---

# docker基于Nginx配置TCP负载均衡

## 给出Nginx的dockerfile
该dockerfile文件只支持TCP协议负载均衡,在编译的时候去掉了http(已经去除禁用http功能，放开tcp、http功能).

```dockerfile
#基础镜像
FROM centos:7

#维护人员信息
MAINTAINER eureka "euka.news@163.com"

#set time zone and install gcc etc..
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && yum -y install gcc gcc-c++ make automake cmake && yum install gcc gcc-c++ ncurses-devel bison bison-devel -y && yum install -y pcre pcre-devel && yum install -y zlib zlib-devel && yum install -y openssl openssl-devel && yum -y install wget

#设置工作目录，这个命令是用来切换工作目录的，相当于cd命令
WORKDIR /usr/local/src

RUN wget http://nginx.org/download/nginx-1.14.0.tar.gz && tar zxf /usr/local/src/nginx-1.14.0.tar.gz && rm -rf /usr/local/src/nginx-1.14.0.tar.gz

WORKDIR /usr/local/src/nginx-1.14.0

RUN ./configure \
--prefix=/usr/local/nginx \
--conf-path=/usr/local/nginx/conf/nginx.conf \
--pid-path=/usr/local/nginx/conf/nginx.pid \
--error-log-path=/usr/local/nginx/log/error.log \
--with-stream && make && make install
#--without-http && make && make install

COPY nginx/nginx.conf /usr/local/nginx/conf/

#暴露端口
EXPOSE 80

#启动容器
ENTRYPOINT /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf && tail -f /usr/local/nginx/log/error.log

```
## 给出Nginx配置文件

```conf
stream {
    server {
        listen 80;
        proxy_pass app;
    }
 
    upstream app {
        server 192.168.2.108:10010;
        server 192.168.2.108:10011;
        server 192.168.2.108:10012;
        server 192.168.2.108:10013;
    }
}


events {
  worker_connections  20240;  ## Default: 1024
}

 http {
     upstream cmdservcie {
         server 192.168.2.108:10020;
         server 192.168.2.108:10021;
         server 192.168.2.108:10022;
         server 192.168.2.108:10023;
     }
     server {
         listen   8080;
         server_name iotserver;
         location / {
         limit_except GET {
             deny   all;
         }
         proxy_pass http://cmdservcie;
         }
     }
 } 

```
从上面给出的配置文件可以知道,我们会同时有四个服务,下次依次给出服务的dockerfile.

## 基于Java-Tomcat服务的dockerfile

```dockerfile
#基础镜像
FROM centos:7

#维护人员信息
MAINTAINER eureka "euka.news@163.com"

#设置工作目录，这个命令是用来切换工作目录的，相当于cd命令
WORKDIR /usr/local

#上篇文章中已经下载了jdk，为了节省时间我这里使用COPY命令将宿主机中的jdk压缩包复制到镜像中，这样做存在的问题是使用Dockerfile创建镜像的宿主机必须在对应的路
#径下有这个包。我这里的包和Dockerfile文件在同一个目录下，源文件的路径需要是Dockerfile文件所在目录(上下文根目录)的相对路径
#也可以使用wget、 apt-get等命令在线下载
COPY jdk-8u171-linux-x64.tar.gz /usr/local/
#安装tomcat，同JDK
COPY apache-tomcat-8.0.49.tar.gz /usr/local/

RUN mkdir tomcat && mkdir java && tar zxf /usr/local/apache-tomcat-8.0.49.tar.gz -C /usr/local/tomcat && rm -rf /usr/local/apache-tomcat-8.0.49.tar.gz && tar zxf /usr/local/jdk-8u171-linux-x64.tar.gz -C /usr/local/java && rm -rf /usr/local/jdk-8u171-linux-x64.tar.gz && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

#copy app war
#COPY iotserver.war /usr/local/tomcat/apache-tomcat-8.0.49/webapps/

#设置环境变量
ENV JAVA_HOME /usr/local/java/jdk1.8.0_171
ENV PATH $PATH:$JAVA_HOME/bin

#暴露tomcat的内部端口，如果没有修改tomcat的配置文件的话，默认是8080端口
EXPOSE 8080

#启动容器时，执行脚本文件启动Tomcat并持续输出日志，防止容器退出。
ENTRYPOINT /usr/local/tomcat/apache-tomcat-8.0.49/bin/startup.sh && tail -f /usr/local/tomcat/apache-tomcat-8.0.49/logs/catalina.out

```
## 依次build dockerfile并启动容器.

```bash
# docker run -d \
    --name=iot-server1-1 \
    --hostname=iot-server1-1 \
    --restart=always \
    --privileged=true \
    -p 10010:8099 \
    -p 10020:8080 \
    eureka/iot-server:1.1

# docker run -d \
    --name=iot-server2-2 \
    --hostname=iot-server2-2 \
    --restart=always \
    --privileged=true \
    -p 10011:8099 \
    -p 10021:8080 \
    eureka/iot-server:1.1

# docker run -d \
    --name=iot-server3-3 \
    --hostname=iot-server3-3 \
    --restart=always \
    --privileged=true \
    -p 10012:8099 \
    -p 10022:8080 \
    eureka/iot-server:1.1

# docker run -d \
    --name=iot-server4-4 \
    --hostname=iot-server4-4 \
    --restart=always \
    --privileged=true \
    -p 10013:8099 \
    -p 10023:8080 \
    eureka/iot-server:1.1

# docker build -t eureka/nginx-tcp:1.1 .

#只有tcp代理
# docker run -d \
    --name=nginx-iot-server \
    --hostname=nginx-iot-server \
    --restart=always \
    --privileged=true \
    -p 8099:80 \
    eureka/nginx-tcp:1.1

#包含http反向代理
# docker run -d \
    --name=nginx-all-iot-server \
    --hostname=nginx-all-iot-server \
    --restart=always \
    --privileged=true \
    -p 8099:80 \
    -p 8080:8080 \
    eureka/nginx-all:1.1
```
依次启动四个服务,然后build我们的nginx dockerfile,命名镜像文件并执行.

- 注:
- 由于link一直出现ping不通现象,采用了统一映射到宿主机端口.