#CentOS7 配置163yum源

- 1.下载163repo文件
```
wget http://mirrors.163.com/.help/CentOS7-Base-163.repo
```

- 2.备份并切换系统的repo文件
```
#备份系统repo文件
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak
#替换系统repo文件
mv CentOS7-Base-163.repo /etc/yum.repos.d/CentOS-Base.repo
```

- 3.执行yum源更新命令
```
yum clean all
yum makecache
#yum update
```
