## docker搭建postgresql

> postgresql
```bash
## windows
# docker run --name some-postgres --privileged=true -e POSTGRES_USER=root -e POSTGRES_PASSWORD=. -v PGDATA:/d/docker-data/postgres9.6-data -p 5432:5432 -d postgres:9.6-alpine

## linux
# docker run --name some-postgres --privileged=true -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -v PGDATA:/usr/local/data/postgres9.6-data -p 5432:5432 -d postgres:9.6-alpine
```
- PGDATA 为data文件挂在路径，如果docker安装在win10上，挂载在D盘的写法为：
```conf
# /d/docker-data/postgres9.6-data
```
如果挂载在linux上，路径则可以是：
```conf
# /var/local/postgres9.6-data
```

> postgis
```bash
## windows
# docker run --name postgis-db --privileged=true -e POSTGRES_USER=root -e POSTGRES_PASSWORD=. -v PGDATA:/d/docker-data/postgis9.6-data -p 5432:5432 -d mdillon/postgis:9.6-alpine

## 默认用户名：postgres
# docker run --name postgis-db --privileged=true -e POSTGRES_PASSWORD=. -v PGDATA:/d/docker-data/postgis9.6-data -p 5432:5432 -d mdillon/postgis:9.6-alpine

## linux
# docker run --name postgis-db --privileged=true -e POSTGRES_USER=root -e POSTGRES_PASSWORD=. -v PGDATA:/usr/local/data/postgis9.6-data -p 5432:5432 -d mdillon/postgis:9.6-alpine

## 默认用户名：postgres
# docker run --name postgis-db --privileged=true -e POSTGRES_PASSWORD=. -v PGDATA:/usr/local/data/postgis9.6-data -p 5432:5432 -d mdillon/postgis:9.6-alpine
```

> pgadmin4

```bash
## 拉取images
# docker pull dpage/pgadmin4:3.6

## 邮箱为登录账号
# docker run --name pgadmin4 --privileged=true --link postgis-db:postgis -p 10080:80 -e "PGADMIN_DEFAULT_EMAIL=eureka.shao@gaialab.ai" -e "PGADMIN_DEFAULT_PASSWORD=." -d dpage/pgadmin4:3.6
```