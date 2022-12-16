from locate3 import get_points
from imutils.perspective import four_point_transform
import cv2,sys,time
import numpy as np


img_path ="crop/"+sys.argv[1]
# img_path="photo/"+input("請輸入照片檔名(會自動填入路徑)：")
image = cv2.imread(img_path, cv2.IMREAD_COLOR)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
# image=cv2.GaussianBlur(image,(5,5),10)
# ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

t1=time.monotonic()

def transformation(points=get_points(img_path)):
    four_points =points
    for i in range(0,3):
        cv2.line(image, points[i], points[i+1], (0, 0, 255),1)
    cv2.line(image, points[0], points[3], (0, 0, 255), 1)
    cv2.imshow("line", image)
    print(points)
    rect = four_point_transform(image, np.array(four_points))
    cv2.imwrite('output.png', rect)
    
    # cv2.imshow("rect", rect)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

transformation()

print("執行時間：",time.monotonic()-t1)