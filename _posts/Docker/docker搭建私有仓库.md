# docker搭建私有仓库

Docke官方提供了Docker Hub网站来作为一个公开的集中仓库。然而，本地访问Docker Hub速度往往很慢，并且很多时候我们需要一个本地的私有仓库只供网内使用。
Docker仓库实际上提供两方面的功能，一个是镜像管理，一个是认证。前者主要由docker-registry项目来实现，通过http服务来上传下载；后者可以通过docker-index（闭源）项目或者利用现成认证方案（如nginx）实现http请求管理。

接下来我们一步一步来实现自己的私有仓库的搭建。

## 环境
- CentOS 7
- Docker Server 1.13.1
- Docker Client 1.13.1

## 安装registry和web管理界面

```bash
docker pull registry:2.6

# 默认run，这样的结果是会把images存放在容器中，如果删除容器，会被同时删除。
docker run -d -p 5000:5000 registry:2.6

#制定宿主机挂载路径，这样的好处是把镜像文件存放在宿主机中。
docker run -d -p 5000:5000 --restart=always --name registry -v /opt/registry:/var/lib/registry registry:2.6

#安装web管理界面
docker run -it -p 5001:8080 --name registry-web --link registry -e REGISTRY_URL=http://registry:5000/v2 -e REGISTRY_NAME=localhost:5000 --restart=always --privileged=true hyper/docker-registry-web
```

## 使用

比如我本地已经从docker.io拉取了Centos：7，怎么把这个镜像push到本地仓库呢？

- 首先，我们需要给景象打一个tag。
  
```bash
## 因为仓库在我本地，所有是localhost，端口是5000，所以完整的是localhost:5000,如果你的是ip地址，请使用IP地址。
# docker tag centos:7 localhost:5000/centos:7
```

- push 镜像文件

```bash
# docker push localhost:5000/centos:7
```

- 拉取
```bash
# docker pull localhost:5000/centos:7
```
如果不在同一台机器上，会报一个 gave http response to https client的错误。这是因为使用registry时，必须使用TLS保证其安全。我们修改client配置，使其能够访问我们的http私有仓库。

编辑/etc/docker/daemon.json文件：
```conf
{ "insecure-registries":["<ip>:5000"] }
```
把<ip>替换为具体的私有仓库ip地址，重启docker，重新push即可。

## 扩展知识：web管理/registry对外接口

```bash
## 获取所有镜像列表
# curl -XGET http://192.168.1.8:5000/v2/_catalog

## 获取某个镜像对应的版本及明细
# curl -XGET http://192.168.1.8:5000/v2/<image_name>/tags/list
```
