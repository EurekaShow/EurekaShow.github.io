# docer配置Jenkins

### 下载JDK & Maven
下载[Maven](http://mirrors.cnnic.cn/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz)，解压并拷贝到要挂载的目录
```bash
# mkdir -p /data/docker/jenkins/maven && tar zxf apache-maven-3.3.9-bin.tar.gz && mv ./apache-maven-3.3.9 /data/docker/jenkins/maven
```
下载[JDK](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)，解压并开背到要挂载目录
```bash
# mkdir -p /data/docker/jenkins/java/jdk && tar zxf jdk*.tar.gz && mv ./jdk*/ /data/docker/jenkins/java/jdk
```

### docker run
```bash
# docker run -d --name jenkins \
    --privileged=true \
    -p 9207:8080 \
    -p 50000:50000 \
    -v /data/docker/jenkins/jenkins:/var/jenkins_home \
    -v /data/docker/jenkins/maven/apache-maven-3.3.9:/usr/local/maven \
    -v /data/docker/jenkins/java/jdk:/usr/local/jdk \
    jenkins:2.60.3
```