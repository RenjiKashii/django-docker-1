<h1 align=center>Database Operations</h1>

# 1. MySQL イメージの作成

MySQL を Docker のコンテナとして利用する。

## 1.1. `docker-compose.yml`への変更

```diff
 version: "3.8"
 services:
   app:
    image: app:django
     build: .
     volumes:
       - .:/django
     ports:
       - 8000:8000
     container_name: django_container
     command: python manage.py runserver 0.0.0.0:8000
+    links:
+      - mysql
+    depends_on:
+      - mysql
+
+  mysql:
+    image: mysql:5.7
+    container_name: mysql_host
+    restart: always
+    environment:
+      MYSQL_ROOT_PASSWORD: An1a-Am1pe-a0aj1
+      MYSQL_DATABASE: app
+      MYSQL_USER: user
+      MYSQL_PASSWORD: p@ssw0rd
+      TZ: "Asia/Tokyo"
+    command: mysqld --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
+    ports:
+      - 3306:3306
+    volumes:
+      - ./mysql:/var/lib/mysql
```

<br>

## 1.2. `Dockerfile`への変更

```diff
 FROM python:3.8-slim-buster
 ENV PYTHONUNBUFFERED=1
 WORKDIR /django
 COPY requirements.txt requirements.txt
-RUN pip3 install -r requirements.txt
+RUN apt-get update && \
+    apt-get install -y default-libmysqlclient-dev build-essential && \
+    rm -rf /var/lib/apt/lists/*
+RUN pip3 install --upgrade pip && \
+    pip3 install -r requirements.txt
+RUN mkdir -p /var/log/mysql
+RUN touch /var/log/mysql/mysqld.log
```

# 2. コンテナの起動

```bash
> docker-compose up -d mysql
# 少し待ってから
> docker-compose up -d app
```

## 2.1. 注意点

`docker-compose up`で起動すると、`mysql`と`app`のコンテナが同時に起動する。  
しかし、`app`は`mysql`が起動していないとエラーを起こす。

そのため、`mysql`コンテナを起動してから、`app`コンテナを起動する。
