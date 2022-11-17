import cv2
import numpy as np
import imutils


def get_points(img):
    print(img)
    image = cv2.imread(img,cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    edged = cv2.Canny(gray, 30,150) #Perform Edge detection
    cv2.imshow('edged',edged)
    cv2.waitKey(0)

    contours=cv2.findContours(edged.copy(),cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours,key=cv2.contourArea, reverse = True)[:20]
    screenCnt = None
    for c in contours:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    print("位置")
    print(screenCnt)

    print(type(screenCnt),screenCnt,screenCnt.shape)
    temp=[]
    for i in range(4):
        temp.append((screenCnt[i][0][0],screenCnt[i][0][1]))
    return temp
