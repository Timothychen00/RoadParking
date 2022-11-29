import cv2
import numpy as np
import imutils,os
from imutils.perspective import four_point_transform
folder='1128'
img_path='capture.jpg'

def do(folder,img_path):
    print(img_path)
    image = cv2.imread(folder+'/'+img_path,cv2.IMREAD_COLOR)
    image=cv2.GaussianBlur(image,(5,5),10)
# ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('edged',image)
    cv2.waitKey(0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    edged = cv2.Canny(gray, 30,150) #Perform Edge detection
    cv2.imshow('edged',edged)
    cv2.waitKey(0)

    contours=cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours,key=cv2.contourArea, reverse = True)[:20]
    screenCnt = np.array([])
    for c in contours:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # approx=cv2.convexHull(c)
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    print("位置")
    print(screenCnt)
    if screenCnt.size:
        temp=[]
        for i in range(4):
            temp.append((screenCnt[i][0][0],screenCnt[i][0][1]))
            if i:
                cv2.line(image, temp[i-1], temp[i], (0, 0, 255),1)
        else:
            cv2.line(image, temp[3], temp[0], (0, 0, 255),1)
        cv2.imshow("line", image)
        rect = four_point_transform(image, np.array(temp))
        print('output1/'+img_path.split('.')[0]+'.png')
        cv2.imwrite('output1/'+img_path.split('.')[0]+'.png', image)
        cv2.imwrite('output1/'+img_path.split('.')[0]+'-cut.png', rect)
        # cv2.imshow("rect", rect)
        cv2.waitKey(0)
    else:
        print('err'+img_path)

    
for i in os.listdir('1128'):
    do(folder,i)