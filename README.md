# DTB-instafacesearch
2023 분산시스템및컴퓨팅 팀프로젝트

환경

● OS : ubuntu 16.04.7  
● hadoop-2.7.1  
● spark-2.3.0  

git clone https://github.com/dbehdrnr0202/DTB-instafacesearch.git  

0. java, hadoop, spark install은 위의 버전으로 설치면 됨  

이후 사용법  

1. 
	```
    cd python_code_tmp
	```    

2. 
   	```
   	sudo chmod -R 755 install_python_and_libraries.sh start.sh stop.sh test.sh train.sh
   	```    
    a. start.sh : start hadoop/spark  
    b. stop.sh : stop hadoop/spark  
    c. train.sh -i executor_number -m executor_memory -s spark_master -h hdfs_location: model train/save to hdfs  
   		usage :  
		```
		./train.sh -i 2 -m 4G // train model with 2 executor instances and each executor will run in 4G memory
		```  
		option  
		-i : executor instance number --default: 2
		-m : executor instance memory --default: 4G
		-s : spark_master --default: spark://master:7077  
		-h : hdfs_location --default: hdfs://master:9000  
    d. test.sh -i executor_number -m executor_memory -s spark_master -h hdfs_location: model load from hdfs and test image files  
		usage : same as train.sh  
    e. install_python_and_libraries.sh : python 3.6.15 설치 및 필요 라이브러리 설치용 shell file    

3.  python 3.6.15 설치 및 필요 라이브러리들 설치
	```
   	./install_python_and_libraries.sh
   	```  

4. check version with ```python -V```  
    must be 3.6.15    

5.  instacrawl.py를 실행하여 instagram 계정의 crawling을 진행한다.  
	code/crawling_img/accounts.txt에 crawling을 할 대상의 계정 정보가 존재한다.  
	이를 수정함으로써 crawling 대상을 추가/삭제할 수 있다.  
	```
	python instacrawl.py user_instagram_id user_instagram_password
	```  
	required parameter  
	user_instagram_id : 사용자의 instagram id이다.  
	user_instagram_passwod : 사용자의 instagram password이다.  
	위의 정보를 제대로 입력해야 instagram에 접근하여 crawling을 제대로 수행할 수 있다.
크롤링을 했을 경우 img_crop에 파일이 추가된다.  

6. face_crop.py를 실행하여 crawling한 sns 사진들에 존재하는 얼굴들을 추출하여 인물 얼굴 이미지를 저장한다.
	```
	python face_crop.py
	```

7.  추가된 파일들을 통해 train을 하고 싶을 경우 train.sh를 실행한다  
	train.sh는 img_crop에 저장되어있는 파일들을 hdfs의 train폴더 내부로 업로드한 뒤, train_save_model.py를 실행하여 모델을 학습시킨 뒤, hdfs/train/lr에 모델을 저장한다.
   	```
   	./train.sh -i executor_number -m executor_memory -s spark_master -h hdfs_location: model train/save to hdfs  
   	```    

8. python_code_tmp 내부에 test_img 폴더를 생성한 뒤, 테스트할 파일들을 올린다.  

9.  test.sh를 실행하여 test_img내부에 존재하는 이미지 파일들을 hdfs에 올린 뒤, test_load_model.py가 실행되어 저장했던 모델을 갖고온 뒤, 이미지의 labeling을 진행한다.
   	```
   	./test.sh -i executor_number -m executor_memory -s spark_master -h hdfs_location: load model from hdfs and test images    
   	```    

10. 모든 작업이 끝났을 경우 stop.sh를 통해 hadoop과 spark를 종료한다.
    ```
   	./stop.sh
   	```    
----------  이전 ----------  




● OS : ubuntu 16.04.7

● hadoop-3.3.0
(실습 2장 교재 참고)

● spark-3.3.2
(실습 5장 교재 참고)

● zookeeper 3.7.1  
(설치 방법 출처:https://phoenixnap.com/kb/install-apache-zookeeper)

1. java installaion test  
java -version

1. make superuser for zookeeper  
$ sudo useradd zookeeper -m  
$ sudo usermod --shell /bin/bash zookeeper  
$ sudo passwd zookeeper  
$ sudo usermod -aG sudo zookeeper  
$ sudo getent group sudo  

1. download and install zookeeper  
$ sudo mkdir -p /data/zookeeper  
$ sudo chown -R zookeeper:zookeeper /data/zookeeper  
$ cd /opt  
$ sudo wget https://dlcdn.apache.org/zookeeper/zookeeper-3.7.1/apache-zookeeper-3.7.1-bin.tar.gz --no-check-certificate  
$ sudo tar -xvf apache-zookeeper-3.7.1-bin.tar.gz 
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

1. execute zookeeper  
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

/*
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

*/

● python 3.5.2  

0. ubuntu 16.04에는 python 3.5.2과 2.7.2가 깔려있음.
python3 --version
> python 3.5.2 인지 확인.  

2. pip 설치 및 업그레이드  
sudo apt-get install python3-pip  
python -m pip install --upgrade pip==20.3  <- 한 번에 업데이트를 하면 오류가 남. 업뎃을 두 단계로 나눠서 진행.
python -m pip install --upgrade pip  
python -m pip --version  
> 여기서 pip 20.3.4인 것을 확인.  

2. 기본 python 및 pip를 최신화  
sudo ln -s /usr/bin/python3 /usr/bin/python  
sudo ln -s /usr/bin/pip3 /usr/bin/pip  
> $ python --version 및 $ pip --version 할 때 3.5.2, 20.3.4인지 
