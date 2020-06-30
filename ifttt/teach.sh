
model="/home/ftp/storage/model/keras_model.h5"
label="/home/ftp/storage/model/labels.txt"
camerafolder="/home/ftp/sdcard/Camera1/"
ifttt_link="https://maker.ifttt.com/trigger/MotionCam/with/key/ddMmb_mQAvNb2lKKf0tHz8IC1s4NE_8LWTJe5iIf6h-"


#get the latest image [DO NOT CHANGE ANYTHING BEBLOW
directory=`ls -Rtrl $camerafolder | grep ":$" | tail -1 | sed 's/://g'`
imgfile=`ls -Rtrl $camerafolder | tail -1 | cut -c 58-`
ifile="${directory}/${imgfile}"
#echo $ifile

# get teachable machine predication 
pred=`curl -s -u lbai:test -F "picture=@$ifile" -F "model=@$model"  -F "class=@$label" -F "format=text" http://templebits.duckdns.org/classfy`

sendcmd='{"value1": "'$pred'"}'
curl -s -X POST -H "Content-Type: application/json" -d "$sendcmd" $ifttt_link
 

