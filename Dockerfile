FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
RUN mkdir -p /var/log/mysql
RUN touch /var/log/mysql/mysqld.log