sudo wget https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tar.xz
sudo tar xvf Python-3.6.15.tgz
cd Python-3.6.15
./configure --enable-optimizations
sudo make altinstall
sudo ln -s /usr/local/bin/python3.6 /bin/python
python -V

python -m pip install h5py==2.10.0
python -m pip install keras==2.1.5
python -m pip install numpy==1.19.5
python -m pip install pandas==1.1.5
python -m pip install py4j==0.10.9.5
python -m pip install sparkdl==0.2.2
python -m pip install tensorflow==1.4.0
python -m pip install tensorflowonspark==2.2.5
python -m pip install pyspark==2.3.0
python -m pip install selenium
python -m pip install webdriver_manager
python -m pip install face_recognition
python -m pip install PIL