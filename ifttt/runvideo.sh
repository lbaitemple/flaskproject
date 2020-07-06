rm test.jpg
ffmpeg -i http://192.168.86.22:8081 -vframes 1   test.jpg
curl -u mike:test -F "img=@test.jpg" http://templebits.duckdns.org/uploadfeed
sleep 1