# flaskproject
```
curl -u lbai:test -F "picture=@pic2.jpg"   -F "format=text"  -F "model=@keras_model.h5" -F "class=@labels.txt"  http://templebits.duckdns.org/classfy
```

# load into aws 
```
cd ~
git clone https://github.com/lbaitemple/flaskproject
cd ~/flaskproject
sudo /bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=1024
sudo /sbin/mkswap /var/swap.1
sudo /sbin/swapon /var/swap.1
chmod +x ./linux_install.sh 
./linux_install.sh
```
### To enable swap memory
```
sudo echo "/swap1 swap swap" >> /etc/fstab
```

### To remove the swap memory

```
sudo swapoff /var/swap.1
sudo rm /var/swap.1
```

# create a new root user and restart the server
```
cd ~/flaskproject
source venv/bin/activate
python createroot.py -p yourpasswd
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
