<h1 align=center>Django with Docker Compose</h1>

# 0. Prerequisite

1. Docker Desktop on Mac がインストールされていること

<br>

# 1. Preparation

## 1.1. `Dockerfile`の作成

```docker
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
```

### 1.1.1. `-buster`とは

Debian Release をベースに構築されたイメージである。

<br>

### 1.1.2. `-slim`とは

Linux 系 OS のフルイメージの下位互換バージョンである。  
インストール済みのパッケージは最低限であり、軽量化されている。

### 1.1.3. `PYTHONUNBUFFERED=1`とは

コンテナの Python の出力(コンテナログ)を標準出力と標準エラー出力に出力するようにする？

<br>

# 2. `docker-compose.yml`の作成

```yml
version: "3.8"
services:
  app:
    build: .
    volumes:
      - .:/django
    ports:
      - 8000:8000
    image: app:django
    container_name: django_container
    command: python manage.py runserver 0.0.0.0:8000
```

# 3. イメージを作成する

```bash
> docker-compose build
```

<br>

# 4. Python のコマンドを利用する

```bash
> docker-compose run --rm app django-admin startproject core .
# docker-compose run --rm [image_name] [command]
```

## 4.1. `--rm`とは

コンテナを停止した際に、そのコンテナを削除する。  
もし削除しないと、毎回新しいコンテナが作成される。

## 4.2. `docker-compose run`とは

例えば、Django が用意している django-admin コマンドを利用したいとする。  
しかし、当然作業しているディレクトリには、Django はインストールされておらず、このコマンドは利用できない。  
仮に、利用できるようにしていたとしても、実際に Docker で動作させる Python のバージョンや OS の違いにより、挙動が違うかもしれない。

このコマンドは、イメージからコンテナを１度構築し、コンテナから任意のコマンドを実行する。  
そのため、実際にコンテナで動作する Python や Django により、コマンドは実行される。

そのため、もしローカルに、Python や Django がインストールされていなくとも、問題ない。

また、このコマンドは、`docker-compose.yml`で指定したポートを作成しない。  
そのため、ポートの衝突を気にせずにコマンドを実行できる。

<br>

# 5. コンテナを構築、起動する

```bash
docker-compose up

# バックグランドでコンテナを実行する場合
docker-compose up -d
```

# 6. 参考サイト

[本堂俊輔の IT エンジニアチャネル | django チュートリアル](https://www.youtube.com/watch?v=nS41IkL13QE&list=PLuCS8p0T7ozK4Ne1e5eAVG2R5Gbs1naix&ab_channel=%E6%9C%AC%E5%A0%82%E4%BF%8A%E8%BC%94%E3%81%AEIT%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%83%81%E3%83%A3%E3%83%B3%E3%83%8D%E3%83%AB)

[Very Academy | Docker Mastery with Django](https://www.youtube.com/watch?v=W5Ov0H7E_o4&list=PLOLrQ9Pn6cazCfL7v4CdaykNoWMQymM_C&ab_channel=VeryAcademy)
