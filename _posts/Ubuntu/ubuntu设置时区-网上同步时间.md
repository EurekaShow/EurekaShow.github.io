# ubuntu设置时区，网上同步时间

Linux默认情况下使用UTC格式作为标准时间格式，如果在Linux下运行程序，且在程 序中指定了与系统不一样的时区的时候，可能会造成时间错误。如果是Ubuntu的桌面版，则可以直接在图形模式下修改时区信息，但如果是在Server版 呢，则需要通过tzconfig来修改时区信息了。使用方式(如将时区设置成Asia/Chongqing)：

sudo tzconfig，如果命令不存在请使用 dpkg-reconfigure tzdata

然后按照提示选择 Asia对应的序号，选完后会显示一堆新的提示—输入城市名，如Shanghai或Chongqing，最后再用 sudo date -s “” 来修改本地时间。
按照提示进行选择时区，然后：
```
sudo cp /usr/share/zoneinfo/Asia/ShangHai /etc/localtime
```
上面的命令是防止系统重启后时区改变。
网上同步时间

1.  安装ntpdate工具
```bash
# sudo apt-get install ntpdate
```
2.  设置系统时间与网络时间同步
```bash
# ntpdate cn.pool.ntp.org
```
3.  将系统时间写入硬件时间
```bash
# hwclock –systohc
```
cn.pool.ntp.org是位于中国的公共NTP服务器，用来同步你的时间(如果你的时间与服务器的时间截不同的话，可能无法同步时间哟，甚至连sudo reboot这样的指令也无法执行)。