import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt


def get_points(img):
    print(img)
    image = cv2.imread(img,cv2.IMREAD_COLOR)
    cv2.imshow('edged',image)
    cv2.waitKey(0)

    gray_img=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    GaussianBlur_img=cv2.GaussianBlur(gray_img,(3,3),0)
    Sobel_img=cv2.Sobel(GaussianBlur_img,-1,1,0,ksize=3)
    ret,binary_img=cv2.threshold(Sobel_img,127,255,cv2.THRESH_BINARY)

    kernel=np.ones((5,15),np.uint8)

  

    close_img=cv2.morphologyEx(binary_img,cv2.MORPH_CLOSE,kernel)
    open_img=cv2.morphologyEx(close_img,cv2.MORPH_OPEN,kernel)

    element=cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
    dilation_img=cv2.dilate(open_img,element,iterations=3)

    
    cv2.imshow('edged',dilation_img)
    cv2.waitKey(0)

    contours=cv2.findContours(dilation_img.copy(),cv2.RETR_TREE,
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
