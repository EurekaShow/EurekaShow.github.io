# docker搭建常用工具

### Java-Tomcat-IotServer

- 给予JDK8，Tomcat8的服务容器
```bash
# docker run -it --name iot-server --restart=always  --privileged=true  -p 8080:8080 -p 8099:8099 iot-server:1.0 /bin/bash
```