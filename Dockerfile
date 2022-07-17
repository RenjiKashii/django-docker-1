FROM python:3.8-slim-buster AS dev-build
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential zip unzip curl && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
RUN curl -fsSL https://deb.nodesource.com/setup_17.x | bash -
RUN apt-get install -y nodejs
RUN npm install npm@latest -g
RUN mkdir -p /var/log/mysql
RUN touch /var/log/mysql/mysqld.log