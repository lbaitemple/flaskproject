#!/bin/bash
# Install script for Teachable Machine Server on AWS
# Author: Li Bai
# lbai@temple.edu

cd ~/flaskproject
sudo apt update && sudo apt-get upgrade -y
sudo apt-get install python3-pip -y
sudo apt install virtualenv -y
sudo apt-get install apache2 libapache2-mod-wsgi-py3 -y
pip3 install virtualenv
virtualenv --python=python3 venv
source venv/bin/activate
pip install Flask
pip install  Flask-HTTPAuth==4.1.0
pip install tensorflow==2.2.0
pip install numpy==1.16
pip install pillow pandas
pip install paho-mqtt
mkdir -p ~/flaskproject/upload
mkdir -p ~/flaskproject/webpa
sudo chgrp -R www-data ~/flaskproject/
sudo chgrp www-data ~/flaskproject/passwd.txt
sudo cp ./conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
sudo cp ./conf/wsgi.conf /etc/apache2/mods-enabled/
sudo ln -sT ~/flaskproject /var/www/html/flaskproject
sudo apachectl restart
echo "Done!"
echo "To activate your virtual environment, use command 'source venv/bin/activate'."
echo "To exit your virtual enviroment, use command 'deactivate'."
