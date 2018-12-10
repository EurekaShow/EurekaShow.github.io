# CentOS更新系统时间

## 查看时间
```
[root@euka ~]# date
```

## 查看时区
```
[root@euka ~]# date "+%Z"
# or
[root@euka ~]# cat /etc/sysconfig/clock
ZONE="Asia/Hong_Kong"
```

## 设置时区
```
#把当前时区调整为上海就是+8区,想改其他时区也可以去看看/usr/share/zoneinfo目
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

## 同步网络时间
```
ntpdate -u ntp.api.bz
```
如果提示：no command find，那么需要安装下ntdate。
```
yum install -y ntpdate
```

ntp常用服务器：
中国国家授时中心：210.72.145.44
NTP服务器(上海) ：ntp.api.bz
美国： time.nist.gov
复旦： ntp.fudan.edu.cn
微软公司授时主机(美国) ：time.windows.com
北京邮电大学 : s1a.time.edu.cn
清华大学 : s1b.time.edu.cn
北京大学 : s1c.time.edu.cn
台警大授时中心(台湾)：asia.pool.ntp.org