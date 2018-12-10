# CentOS7 禁用SELinux

## 查看SELinux状态：
  
- 1
```bash
  /usr/sbin/sestatus -v      
##如果SELinux status参数为enabled即为开启状态
SELinux status:                 enabled
```

 - 2
```bash
  getenforce                 ##也可以用这个命令检查
```

## 关闭SELinux：
  
- 临时关闭（不用重启机器）：
```bash
setenforce 0                 
##设置SELinux 成为permissive模式
##setenforce 1 设置SELinux 成为enforcing模式
```

- 永久关闭：  
修改/etc/selinux/config 文件
```bash
#将
SELINUX=enforcing
#改为
SELINUX=disabled
```
重启机器即可
