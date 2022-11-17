from locate import get_points
from imutils.perspective import four_point_transform
import cv2,sys
import numpy as np

img_path = sys.argv[1]
image = cv2.imread(img_path, cv2.IMREAD_COLOR)

def transformation(points=get_points(img_path)):
    four_points =points
    rect = four_point_transform(image, np.array(four_points))
    cv2.imwrite('output.png', rect)
    cv2.imshow("rect", rect)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

transformation()

