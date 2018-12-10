#基础镜像
FROM centos:7

#维护人员信息
MAINTAINER eureka "euka.news@163.com"

#set time zone
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
--with-stream  && make && make install

COPY nginx/nginx.conf /usr/local/nginx/conf/

#暴露端口
EXPOSE 80

#启动容器
ENTRYPOINT /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf && tail -f /usr/local/nginx/log/error.log
