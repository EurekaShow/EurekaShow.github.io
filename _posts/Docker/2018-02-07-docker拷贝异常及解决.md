# docker拷贝异常及解决

- docker容器和宿主机之间拷贝方法

```bash 

#拷贝到容器
# docker cp 宿主路径/文件 容器id:路径/文件

#从容器拷贝出
# docker cp 容器id:路径/文件 宿主路径/文件
```

- cp会报一个异常：Error: Path not specified。

系统和docker版本信息为：
```bash
[root@localhost ~]# uname -a
Linux localhost.localdomain 4.4.133-1.el6.elrepo.x86_64 #1 SMP Sat May 26 10:25:53 EDT 2018 x86_64 x86_64 x86_64 GNU/Linux
[root@localhost ~]# cat /etc/issue
CentOS release 6.9 (Final)
Kernel \r on an \m

[root@localhost ~]# docker version
Client version: 1.7.1
Client API version: 1.19
Go version (client): go1.4.2
Git commit (client): 786b29d/1.7.1
OS/Arch (client): linux/amd64
Server version: 1.7.1
Server API version: 1.19
Go version (server): go1.4.2
Git commit (server): 786b29d/1.7.1
OS/Arch (server): linux/amd64
[root@localhost ~]#

```

- 处理办法：

直接将文件更新至容器在宿主机的目录，其目录为：

```bash
# /var/lib/docker/devicemapper/mnt/<容器id>/rootfs/

# 如：
# /var/lib/docker/devicemapper/mnt/38165d8df50b1e24de2f5add5387602d9140af815ead7e3b40e2d42e317b5a94/rootfs/
```
