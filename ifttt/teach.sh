
model="/home/ftp/storage/model/keras_model.h5"
label="/home/ftp/storage/model/labels.txt"
camerafolder="/home/ftp/sdcard/Camera1/"
ifttt_link="https://maker.ifttt.com/trigger/MotionCam/with/key/ddMmb_mQAvNb2lKKf0tHz8IC1s4NE_8LWTJe5iIf6h-"
webcamurl=http://192.168.86.22:8081 
youtubekey=""
value2="test"

#get the latest image [DO NOT CHANGE ANYTHING BEBLOW
directory=`ls -Rtrl $camerafolder | grep ":$" | tail -1 | sed 's/://g'`
imgfile=`ls -Rtrl $camerafolder | tail -1 | cut -c 58-`
ifile="${directory}/${imgfile}"
#echo $ifile

# get teachable machine predication 
pred=`curl -s -u lbai:test -F "picture=@$ifile" -F "model=@$model"  -F "class=@$label" -F "format=text" http://templebits.duckdns.org/classfy`

#echo $pred
# send the result to IFTTT
sendcmd='{"value1": "'$pred'", "value2" : "'$value2'"}'
curl -s -X POST -H "Content-Type: application/json" -d "$sendcmd" $ifttt_link
 
 curl https://raw.githubusercontent.com/lbaitemple/motioneye2youtube/master/livestream.sh --output livestream.sh

curl https://raw.githubusercontent.com/lbaitemple/motioneye2youtube/master/livestream.sh --output livestream.sh
bash /home/ftp/storage/livestream.sh $webcamurl $youtubekey
