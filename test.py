import yolov4.detect
import time
import testtt

t1=time.monotonic()
# image='output/44:17:93:7E:3B:7C.jpg'
# yolov4.detect.main(image)
# yolov4.detect.main(image)

testtt.recognize('44:17:93:7E:3B:7C')
t2=time.monotonic()
print('total_time:',t2-t1,'s')