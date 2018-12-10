# raspberry设置python脚本开机启动

- 1.开机启动脚本

保存脚本为 /etc/init.d/sendemail
该脚本使用前提为我已经写好了一个自动发送邮件的python脚本，完整路径为：
/usr/local/python-proj/timer_send_email.py

```bash
#!/bin/bash
# /etc/init.d/sendemail

### BEGIN INIT INFO
# Provides: embbnux
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: sendemail initscript
# Description: This service is used to manage a led
### END INIT INFO

case "$1" in
    start)
        echo "Starting Send Email"
        /usr/local/python-proj/timer_send_email.py &
        ;;
    stop)
        echo "Stopping Send Email"
        #killall sendemail.py
        kill $(ps aux | grep -m 1 '/usr/local/python-proj/timer_send_email.py' | awk '{ print $2 }')
        ;;
    *)
        echo "Usage: service sendemail start|stop"
        exit 1
        ;;
esac
exit 0
```

- 2.设置脚本权限

```bash
root@raspberrypi:~# sudo chmod +x /etc/init.d/sendemail
```

- 3.设置开机启动

```bash
root@raspberrypi:~# sudo update-rc.d sendemail defaults
```

- 4.使用服务

除了实现开机自启动，以后我们还可以使用以下命令：

```bash
root@raspberrypi:~# sudo service sendemail start #启动
root@raspberrypi:~# sudo service sendemail stop #停止
```