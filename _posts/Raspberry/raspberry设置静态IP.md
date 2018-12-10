## raspberry 设置静态IP

```bash
$ sudo vim /etc/dhcpcd.conf
```
*修改/etc/network/interfaces已经无效*

添加配置文件如下：

```conf
interface wlan0
static ip_address=192.168.1.82/24
static routers=192.168.1.1
static domain_name_servers=202.102.152.3 114.114.114.114
```

interface 后面的内容即为网卡名称，ifconfig后，可以看到所有网卡，针对正在使用的网卡修改即可。