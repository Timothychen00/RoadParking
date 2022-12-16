import yolov4.detect
import time
import testtt

t1=time.monotonic()
image='yolov4/data/images/capture.jpg'
yolov4.detect.main(image)
# yolov4.detect.main(image)

testtt.recognize()
t2=time.monotonic()
print('total_time:',t2-t1,'s')