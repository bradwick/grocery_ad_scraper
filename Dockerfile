# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /usr/src/app

RUN sudo apt-get -y update
RUN sudo apt-get -y upgrade
RUN sudo apt-get install -y sqlite3 libsqlite3-dev
RUN mkdir /db
RUN /usr/bin/sqlite3 /db/grocery.db
# make sure to mount db folder /home/dbfolder/:/db imagename

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./api.py"]