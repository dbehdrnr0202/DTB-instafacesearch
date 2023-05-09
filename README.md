# DTB-instafacesearch
2023 분산시스템및컴퓨팅 팀프로젝트

환경

OS : ubuntu 16.04.7

hadoop-3.3.0

spark-3.3.2

zookeeper 3.7.1
(설치 방법 출처:https://phoenixnap.com/kb/install-apache-zookeeper)

0. java installaion test
java --version

1. make superuser for zookeeper
$ sudo useradd zookeeper -m
$ sudo usermod --shell /bin/bash zookeeper
$ sudo passwd zookeeper
$ sudo usermod -aG sudo zookeeper
$ sudo getent group sudo

2. download and install zookeeper
$ sudo mkdir -p /data/zookeeper
$ sudo chown -R zookeeper:zookeeper /data/zookeeper
$ cd /opt
$ sudo wget https://dlcdn.apache.org/zookeeper/zookeeper-3.7.1/apache-zookeeper-3.7.1-bin.tar.gz --no-check-certificate
$ sudo tar -xvf apache-zookeeper-3.7.1-bin
$ sudo mv apache-zookeeper-3.7.1-bin zookeeper
$ sudo chown -R zookeeper:zookeeper /opt/zookeeper
$ sudo vi /opt/zookeeper/conf/zoo.cfg
---(zoo.cfg in vi editer)---
tickTime = 2000
dataDir = /data/zookeeper
clientPort = 2181
initLimit = 5
syncLimit = 2
----------------------------

3. execute zookeeper
$ cd /opt/zookeeper
$ sudo bin/zkServer.sh start
$ sudo bin/zkCli.sh -server 127.0.0.1:2181
$ sudo bin/zkServer.sh stop
