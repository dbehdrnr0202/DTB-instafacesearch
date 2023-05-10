# DTB-instafacesearch
2023 분산시스템및컴퓨팅 팀프로젝트

환경

● OS : ubuntu 16.04.7

● hadoop-3.3.0
(실습 2장 교재 참고)

● spark-3.3.2
(실습 5장 교재 참고)

● zookeeper 3.7.1  
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
----------  

3. execute zookeeper  
$ cd /opt/zookeeper  
$ sudo bin/zkServer.sh start  
$ sudo bin/zkCli.sh -server 127.0.0.1:2181  
$ sudo bin/zkServer.sh stop  

● flume 1.11.0  

sudo wget https://dlcdn.apache.org/flume/1.11.0/apache-flume-1.11.0-bin.tar.gz --no-check-certificate  
sudo tar -vxzf apache-flume*  

sudo cp flume-conf* flume-conf.properties  
sudo cp flume-env.sh.* flume-env.sh  
sudo vi flume-env.sh  
	---(edit)---  
	export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64  
	------------  
sudo vi ~/.profile  
	---(edit)---  
	export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64  
	------------  

sudo vi flume-conf.properties  

sudo vi ~/.bashrc  
	---(edit)---  
	export $FLUME_HOME=/home/apache-flume-1.11.0-bin  
	export PATH=$PATH:$FLUME_HOME/bin  
	------------  
source ~/.bashrc  

● python 3.11.3  
https://dlehdgml0480.tistory.com/8  

1. 기본 프로그램들 설치  
sudo apt-get install build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev  

2.  파이썬 다운로드 및 설치
cd /opt  
sudo wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz  
sudo tar -xzf Python-3.11.3.tgz  
cd Python-3.11.3  
sudo ./configure --enable-optimizations  
sudo make altinstall  

3. 기본 python을 최신 버전으로 변경  
sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1  
ln -s /usr/local/bin/pip3.11 /usr/bin/pip  
