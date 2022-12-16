import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt


def get_points(img):
    print(img)
    image = cv2.imread(img,cv2.IMREAD_COLOR)
    cv2.imshow('edged',image)
    cv2.waitKey(0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    blur = cv2.blur(gray, (15, 15))

    # cv2.imshow('blur',blur)
    # cv2.waitKey(0)

    kernel = np.ones((10,10), np.uint8)
    
    erosion = cv2.erode(blur, kernel, iterations = 1)
    
    edged = cv2.Canny(erosion, 30,150) #Perform Edge detection
    
    cv2.imshow('edged',edged)
    cv2.waitKey(0)

    contours=cv2.findContours(edged.copy(),cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours,key=cv2.contourArea, reverse = True)[:]
    screenCnt = None
    for c in contours:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        points_list=[]
        for i in range(2):
            points_list.append((approx[i][0][0],approx[i][0][1]))
        for point in points_list:
            cv2.circle(image, point,1, (0,255,0), 3)

      
        if len(approx) == 4:
            screenCnt = approx
            break
    plt.imshow(image)
    plt.show()
    print("位置")
    print(screenCnt)

    # print(type(screenCnt),screenCnt,screenCnt.shape)
    temp=[]
    for i in range(4):
        temp.append((screenCnt[i][0][0],screenCnt[i][0][1]))
    return temp
