DATAPATH=video_raw_data
FILESUFFIX=raw_data.json


if [ ! -d "$DATAPATH" ]; then  
  mkdir "$DATAPATH"  
fi

if [ -f "$DATAPATH/bilibili_$FILESUFFIX" ]; then
  rm "$DATAPATH/bilibili_$FILESUFFIX"
  echo "remove $DATAPATH/bilibili_$FILESUFFIX"
fi

if [ -f "$DATAPATH/iqiyi_$FILESUFFIX" ]; then
  rm "$DATAPATH/iqiyi_$FILESUFFIX"
  echo "remove $DATAPATH/iqiyi_$FILESUFFIX"

fi

if [ -f "$DATAPATH/youku_$FILESUFFIX" ]; then
  rm "$DATAPATH/youku$DATAPATH"
  echo "remove $DATAPATH/youku_$FILESUFFIX"
fi


scrapy crawl iqiyiVideoInfo -a data_loc='video_id/iqiyi_unique_id.txt' -o "$DATAPATH/iqiyi_$FILESUFFIX"
echo iqiyi video information extracted

#scrapy crawl bilibiliVideoInfo -a data_loc='video_id/bilibili_unique_id.txt' -o "$DATAPATH/bilibili_$FILESUFFIX"
#echo bilibili video information extracted

#scrapy crawl youkuVideoInfo -a data_loc='video_id/youku_unique_id.txt' -o "$DATAPATH/youku_$FILESUFFIX"
#echo youku video information extracted

#echo all done!!!
