# docker入门-预备之升级Centos 7.x内核
最近在学习 Docker,想在服务器上实践一下.Docker 需要安装在 CentOS 7 64 位的平台，并且内核版本不低于 3.10。 CentOS 7 满足最低内核的要求，但由于 CentOS 7 内核版本比较低，部分功能（如 overlay2 存储层驱动）无法使用，并且部分功能可能不太稳定.需要升级到最新的 CentOS 版本,并且内核也更新到最新的稳定版本.
### 检查当前 CentOS 系统版本
```bash
[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.4.1708 (Core) 
```
### 检查当前 CentOS 系统内核版本
```bash
[root@localhost ~]# uname -sr
Linux 3.10.0-693.17.1.el7.x86_64
```
可以看出当前系统为 CentOS 7.4,系统内核版本为 3.10.
### 运行 yum 命令升级
```bash
[root@localhost ~]# yum clean all
[root@localhost ~]# yum update
```
期间会有确认提示,直接回车确认即可,完整后重启系统即可。
```bash
[root@localhost ~]# reboot
```
### 检查当前 CentOS 系统版本及内核版本
```bash
[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.4.1708 (Core) 
[root@localhost ~]# uname -sr
Linux 3.10.0-693.17.1.el7.x86_64
```
可以看到系统已经更新到当前最新的7.4，但是内核却没有变化，接下来我们需要单独升级内核。
```bash
# 要在 CentOS 7.× 上启用 ELRepo 仓库,请运行:
[root@localhost ~]# rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
[root@localhost ~]# rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
# 仓库启用后，使用下面的命令列出可用的系统内核相关包:
[root@localhost ~]# yum --disablerepo="*" --enablerepo="elrepo-kernel" list available
Loaded plugins: fastestmirror, langpacks
Loading mirror speeds from cached hostfile
 * elrepo-kernel: dfw.mirror.rackspace.com
Available Packages
kernel-lt-devel.x86_64                         4.4.115-1.el7.elrepo                elrepo-kernel
kernel-lt-doc.noarch                           4.4.115-1.el7.elrepo                elrepo-kernel
kernel-lt-headers.x86_64                       4.4.115-1.el7.elrepo                elrepo-kernel
kernel-lt-tools.x86_64                         4.4.115-1.el7.elrepo                elrepo-kernel
kernel-lt-tools-libs.x86_64                    4.4.115-1.el7.elrepo                elrepo-kernel
kernel-lt-tools-libs-devel.x86_64              4.4.115-1.el7.elrepo                elrepo-kernel
kernel-ml.x86_64                               4.15.3-1.el7.elrepo                 elrepo-kernel
kernel-ml-devel.x86_64                         4.15.3-1.el7.elrepo                 elrepo-kernel
kernel-ml-doc.noarch                           4.15.3-1.el7.elrepo                 elrepo-kernel
kernel-ml-headers.x86_64                       4.15.3-1.el7.elrepo                 elrepo-kernel
kernel-ml-tools.x86_64                         4.15.3-1.el7.elrepo                 elrepo-kernel
kernel-ml-tools-libs.x86_64                    4.15.3-1.el7.elrepo                 elrepo-kernel
kernel-ml-tools-libs-devel.x86_64              4.15.3-1.el7.elrepo                 elrepo-kernel
perf.x86_64                                    4.15.3-1.el7.elrepo                 elrepo-kernel
python-perf.x86_64                             4.15.3-1.el7.elrepo                 elrepo-kernel
```
### 接下来我们需要做的就是更新成最新的内核(ml版本安装后可能有问题，这里我们选择lt版本)
```bash
[root@localhost ~]# yum --enablerepo=elrepo-kernel install kernel-lt

#完成所有安装后，重启系统。
[root@localhost ~]# reboot

#启动后，重新查看内核版本
[root@localhost ~]# uname -sr
Linux 4.4.115-1.el7.elrepo.x86_64

#至此，系统内核已经升级成最新的主线稳定内核。
[root@localhost ~]# grub2-set-default 0

#重启系统
[root@localhost ~]# reboot
```
### 至此你可以收手，也可以继续删除之前的旧内核，有强迫症的患者强烈继续哟，病不治疗不痛快。
```bash
#查询所有内核RPM包
[root@localhost ~]# rpm -qa | grep kernel
kernel-3.10.0-693.17.1.el7.x86_64
kernel-3.10.0-693.el7.x86_64 
kernel-tools-libs-3.10.0-693.17.1.el7.x86_64 
kernel-tools-3.10.0-693.17.1.el7.x86_64
kernel-lt-4.4.115-1.el7.elrepo.x86_64
abrt-addon-kerneloops-2.1.11-48.el7.centos.x86_64

#执行remove，因为我的系统是运行在虚拟机中，所有查询中有一个abrt-addon-kerneloops-2.1.11-48.el7.centos.x86_64，记得要排除remove列表。
[root@localhost ~]# yum remove kernel-3.10.0-693.17.1.el7.x86_64 kernel-3.10.0-693.el7.x86_64 kernel-tools-libs-3.10.0-693.17.1.el7.x86_64 kernel-tools-3.10.0-693.17.1.el7.x86_64 
```
### 大功告成，享受新内核带来的乐趣吧～