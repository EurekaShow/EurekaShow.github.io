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
EXPOSE 8090
EXPOSE 8091
EXPOSE 8092
EXPOSE 8093
EXPOSE 8094
EXPOSE 8095

#启动容器时，执行脚本文件启动Tomcat并持续输出日志，防止容器退出。
ENTRYPOINT /usr/local/tomcat/apache-tomcat-8.0.49/bin/startup.sh && tail -f /usr/local/tomcat/apache-tomcat-8.0.49/logs/catalina.out
