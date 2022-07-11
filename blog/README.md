<h1 align=center>Database Operations</h1>

# 1. MySQL イメージの作成

MySQL を Docker のコンテナとして利用する。

<br>

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

<br>

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

# 3. モデルの作成

モデルの定義は、`models.py`に記載する。

<br>

## 3.1. Primary Key について

Primary Key(id)は、自動的に Django により作成される。  
`models.py`には、書かなくてよい。

<br>

## 3.2. マイグレーションについて

`models.py`から作成する。  
便利...

```bash
> docker-compose run --rm app python3 manage.py makemigrations blog
```

## 3.3. migrate を実行する

```bash
> docker-compose run --rm app python3 manage.py migrate
```

## 3.4. Python インタプリタ(Django 用)

```bash
> docker-compose run app python3 manage.py shell
```

## 3.5. モデルのいろいろな操作

```bash
Creating f_app_run ... done
Python 3.8.13 (default, Jun 23 2022, 11:52:37)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

# コンソールが開き、コードをインタラクティブに記載できる.

# 作成したモデルをインポートする.
>>> from blog.models import Category, Tag, Post

# インポートしたモデルを確認.
>>> Category
<class 'blog.models.Category'>
>>> Tag
<class 'blog.models.Tag'>
>>> Post
<class 'blog.models.Post'>

# データを作成する.
>>> Category.objects.create(name="cat_1")
<Category: cat_1>

# データを全件取得する.
>>> Category.objects.all()
<QuerySet [<Category: cat_1>]>

>>> Category.objects.create(name="cat_2")
<Category: cat_2>
>>> Category.objects.all()
<QuerySet [<Category: cat_1>, <Category: cat_2>]>

# 最初の１件のデータのみを取得する.
>>> Category.objects.first()
<Category: cat_1>

# 最初の１件のデータを取得し、cat変数に入れる.
>>> cat = Category.objects.first()
>>> cat
<Category: cat_1>

>>> cat.name
'cat_1'
>>> cat.id
1

# オブジェクトに.
# save()するまでは、DB上には保存されない.
>>> post = Post()
>>> Post()
<Post: >
>>> post.save()

# 保存するデータがないので例外が発生.

Traceback (most recent call last):
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/mysql/base.py", line 75, in execute
    return self.cursor.execute(query, args)
  File "/usr/local/lib/python3.8/site-packages/MySQLdb/cursors.py", line 206, in execute
    res = self._query(query)
  File "/usr/local/lib/python3.8/site-packages/MySQLdb/cursors.py", line 319, in _query
    db.query(q)
  File "/usr/local/lib/python3.8/site-packages/MySQLdb/connections.py", line 254, in query
    _mysql.connection.query(self, query)
MySQLdb.OperationalError: (1048, "Column 'category_id' cannot be null")

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 806, in save
    self.save_base(
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 857, in save_base
    updated = self._save_table(
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 1000, in _save_table
    results = self._do_insert(
  File "/usr/local/lib/python3.8/site-packages/django/db/models/base.py", line 1041, in _do_insert
    return manager._insert(
  File "/usr/local/lib/python3.8/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/query.py", line 1434, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
  File "/usr/local/lib/python3.8/site-packages/django/db/models/sql/compiler.py", line 1621, in execute_sql
    cursor.execute(sql, params)
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 103, in execute
    return super().execute(sql, params)
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/utils.py", line 89, in _execute
    return self.cursor.execute(sql, params)
  File "/usr/local/lib/python3.8/site-packages/django/db/backends/mysql/base.py", line 80, in execute
    raise IntegrityError(*tuple(e.args))
django.db.utils.IntegrityError: (1048, "Column 'category_id' cannot be null")
>>> post.title = "post_1
  File "<console>", line 1
    post.title = "post_1
                       ^
SyntaxError: EOL while scanning string literal

>>> post.title = "post_1"
>>> post.body = "body_1"
>>> post.category = cat
>>> post.save()


>>> Post.objects.all()
<QuerySet [<Post: post_1>]>

# postのtagsは、まだ空なので、このフィールドの説明がでてくる.
>>> post.tags
<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x7faaa9c3cb20>

>>> post.tags.all()
<QuerySet []>

>>> tag1 = Tag.objects.create(name="tag_1")
>>> tag2 = Tag.objects.create(name="tag_2")
>>> Tag.objects.all()
<QuerySet [<Tag: tag_1>, <Tag: tag_2>]>

>>> post.tags.add(tag1)
>>> post.tags.add(tag2)
>>> post.save()

>>> post.tags.all()
<QuerySet [<Tag: tag_1>, <Tag: tag_2>]>

# filterメソッドで、条件に合致したデータのみを取得.
>>> Category.objects.filter(name="cat_1")
<QuerySet [<Category: cat_1>]>

# first()/get()メソッドとも組み合わせられる.
# しかし、get()は意味ない?(filter()だけを記載した場合と挙動同じでは?)
>>> Category.objects.filter(name="cat_1").first()
<Category: cat_1>
>>> Category.objects.filter(name="cat_1").get()
<Category: cat_1>
```
