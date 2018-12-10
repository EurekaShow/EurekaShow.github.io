# Nginx负载均衡TCP-UDP 

## 简介
负载均衡是指有效地跨多个后端服务器分发网络流量。

在版本5及后来版本,NGINX Plus可以代理和负载平衡TCP流量。TCP(传输控制协议)是许多流行的应用程序和服务的协议,如LDAP,MySQL和RTMP。在9或更高版本,NGINX Plus可以代理和负载平衡UDP流量。UDP(用户数据报协议)是许多流行的协议nontransactional应用程序,如DNS,syslog和RADIUS。

## 前提
- 最新开源NGINX使用 --with-stream 配置标识创建,或者最新的NGINX Plus(不需要额外的构建步骤)。
- 应用程序、数据库、或服务在通过TCP或UDP通信。
- 反应服务器,每个运行相同的实例的应用程序,数据库,或服务

## 配置反向代理
打开NGINX配置文件，windows下位于NGINX安装目录\conf\nginx.conf。
- 创建顶级 stream{} 配置块
```
stream{
    #...
}
```
- 在顶级 stream{} 块中为每个虚拟服务器声明一个或多个 server{} 配置块。
```
stream{
    server{
        #...
    }
    server{
        #...
    }
}
```
- 在每个 server{} 配置块中，添加listen节点，用来定义ip地址／端口。在UDP代理类型里，还要添加udp参数。TCP是stream默认的协议内容，所以TCP代理不需要在listen节点处添加tcp字样的参数。
```

stream{
    server{
        listen 12345;
        #...
    }
    server{
        listen 53 udp;
        #...
    }
}
```

``` cmd
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


stream {

    log_format proxy '$remote_addr [$time_local] '
                 '$protocol $status $bytes_sent $bytes_received '
                 '$session_time "$upstream_addr" '
                 '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';

    access_log logs/access.log proxy ;

    server {
        listen 9999;
        proxy_pass kaer_tcp;
    }

    upstream kaer_tcp {
        server 127.0.0.1:10091 weight=2;
        server 127.0.0.1:10092 max_fails=2 fail_timeout=30s;
    }
}
```
