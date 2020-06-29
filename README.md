# flaskproject
```
curl -u lbai:test -F "picture=@pic2.jpg"   -F "format=text"  -F "model=@keras_model.h5" -F "class=@labels.txt"  http://templebits.duckdns.org/classfy
```

# load into aws 
```
git clone https://github.com/lbaitemple/flaskproject
sudo apt update && sudo apt-get upgrade -y
sudo apt-get install python3-pip virtualenv -y
sudo apt-get install apache2 libapache2-mod-wsgi-py3 -y
pip3 install virtualenv
cd flaskproject/
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirement.txt
sudo chgrp www-data ~/flaskproject/
sudo cp conf/000-default.conf /etc/apache2/sites-enabled/000-default.conf
sudo cp conf/wsgi.conf /etc/apache2/mods-enabled/
```

# create a new root user and restart the server
```
python createroot.py -p yourpasswd
sudo chgrp www-data ~/flaskproject/passwd.txt
sudo ln -sT ~/flaskproject /var/www/html/flaskproject
sudo apachectl restart
```


## on your client site
### create other user by add/delete/changepwd
```
curl -u root:yourpasswd -F "action=[add|delete|changpwd]"   -F "user=newuser" -F "passwd=newpasswd"   http://aws-instance_address/user
```

### use your teachable machine model

Picture fils must be specified as JPEG image.
```
curl -u newuser:newpasswd -F "picture=@pic2.jpg"   -F "format=[json|text]"  -F "model=@keras_model.h5" -F "class=@labels.txt"  http://aws-instance_address/classfy
```
model and label files are options if they are loaded into the instance in a previous request, you can specify only the command by using picture file only as
```
curl -u newuser:newpasswd -F "picture=@other.jpg"   -F "format=[json|text]"  http://aws-instance_address/classfy
```

### use the server webhook as MQTT proxies [cloud mqtt, etc]
```
curl -u newuser:newpasswd -F "user=mqtt_user"   -F "passwd=mqtt_passwd" -F "host=m16.cloudmqtt.com" -F "port=12247" -F "topic=topic_mqtt" -F "value=test_value"  http://aws-instance_address/webhook

```
