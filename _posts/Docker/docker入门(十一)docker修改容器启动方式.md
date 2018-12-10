# docker入门(十一)docker修改容器启动方式

当你的容器运行一段时间后,需要修改容器启动方式以便更好的适用新的需求,基于各种理由,你不想重新生成新的容器,那么来看看怎么修改容器启动方式吧.

- 1.update命令
```bash
docker container update --restart=always <containername or id>
```
即可修改为自启动,然后需要做的是重启docker即可.

- 2.修改配置文件


```bash
#通过inspect命令找到容器存放位置:
docker inspect <container id or name>

#修改配置文件
vim vim /var/lib/docker/containers/8b5e6561a994235322e1d9dda32a0155a769ca9e6d4cf3234f2db1c8eb926d1c/hostconfig.json
```
找到一下内容,修改name值为always即可.
```json
"RestartPolicy": {
        "Name": "no",
        "MaximumRetryCount": 0
    }
```
重启动docker.

hostconfig.json文件完整内容大概如下:

```json
{
    "Binds": [],
    "ContainerIDFile": "",
    "LogConfig": {
        "Type": "journald",
        "Config": {}
    },
    "NetworkMode": "bridge",
    "PortBindings": {
        "8080/tcp": [
            {
                "HostIp": "",
                "HostPort": "9205"
            }
        ]
    },
    "RestartPolicy": {
        "Name": "no",
        "MaximumRetryCount": 0
    },
    "AutoRemove": false,
    "VolumeDriver": "",
    "VolumesFrom": null,
    "CapAdd": null,
    "CapDrop": null,
    "Dns": [],
    "DnsOptions": [],
    "DnsSearch": [],
    "ExtraHosts": null,
    "GroupAdd": null,
    "IpcMode": "",
    "Cgroup": "",
    "Links": [
        "/mysql-j:/j/mysql"
    ],
    "OomScoreAdj": 0,
    "PidMode": "",
    "Privileged": true,
    "PublishAllPorts": false,
    "ReadonlyRootfs": false,
    "SecurityOpt": [
        "label=disable"
    ],
    "UTSMode": "",
    "UsernsMode": "",
    "ShmSize": 67108864,
    "Runtime": "docker-runc",
    "ConsoleSize": [
        0,
        0
    ],
    "Isolation": "",
    "CpuShares": 0,
    "Memory": 0,
    "NanoCpus": 0,
    "CgroupParent": "",
    "BlkioWeight": 0,
    "BlkioWeightDevice": null,
    "BlkioDeviceReadBps": null,
    "BlkioDeviceWriteBps": null,
    "BlkioDeviceReadIOps": null,
    "BlkioDeviceWriteIOps": null,
    "CpuPeriod": 0,
    "CpuQuota": 0,
    "CpuRealtimePeriod": 0,
    "CpuRealtimeRuntime": 0,
    "CpusetCpus": "",
    "CpusetMems": "",
    "Devices": [],
    "DiskQuota": 0,
    "KernelMemory": 0,
    "MemoryReservation": 0,
    "MemorySwap": 0,
    "MemorySwappiness": -1,
    "OomKillDisable": false,
    "PidsLimit": 0,
    "Ulimits": null,
    "CpuCount": 0,
    "CpuPercent": 0,
    "IOMaximumIOps": 0,
    "IOMaximumBandwidth": 0
}
```