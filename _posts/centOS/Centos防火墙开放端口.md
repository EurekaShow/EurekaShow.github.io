# Centos防火墙开放端口

## Centos7 防火墙开放端口
```bash
#即时打开，这里也可以是一个端口范围，如1000-2000/tcp
[root@centos7 ~]# firewall-cmd --add-port=3306/tcp　
success

#写入配置文件
[root@centos7 ~]# firewall-cmd --permanent --add-port=3306/tcp
success

#重启防火墙
[root@centos7 ~]# firewall-cmd --reload
success
```
- 开端口
```bash
[root@centos7 ~]# firewall-cmd --add-port=3306/tcp　
```
- 命令含义
- - zone #作用域
- - add-port=80/tcp #添加端口，格式为：端口/通讯协议
- - permanent #永久生效，没有此参数重启后失效

## Centos6 防火墙开放端口

```bash
# 开放指定端口
[root@centos6 ~]# /sbin/iptables -I INPUT -p tcp --dport 80 -j ACCEPT
[root@centos6 ~]# /sbin/iptables -I INPUT -p tcp --dport 22 -j ACCEPT
[root@centos6 ~]# /etc/rc.d/init.d/iptables save
[root@centos6 ~]# /etc/init.d/iptables restart

#或者直接修改防火墙规则
[root@centos6 ~]# vi /etc/sysconfig/iptables

#查看防火墙信息
[root@centos6 ~]# /etc/init.d/iptables status

#关闭防火墙
[root@centos6 ~] #/etc/init.d/iptables stop

#永久关闭防火墙
[root@centos6 ~]# chkconfig –level 35 iptables off

```