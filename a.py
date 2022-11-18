from locate import get_points
from imutils.perspective import four_point_transform
import cv2,sys
import numpy as np

# img_path ="photo/"+sys.argv[1]
img_path="photo/"+input("請輸入照片檔名(會自動填入路徑)：")
image = cv2.imread(img_path, cv2.IMREAD_COLOR)

def transformation(points=get_points(img_path)):
    four_points =points
    for i in range(0,3):
        cv2.line(image, points[i], points[i+1], (0, 0, 255), 5)
    cv2.line(image, points[0], points[3], (0, 0, 255), 5)
    cv2.imshow("line", image)
    print(points)
    rect = four_point_transform(image, np.array(four_points))
    cv2.imwrite('output.png', rect)
    cv2.imshow("rect", rect)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

transformation()

