import cv2
import pytesseract
from separate import cut
import sys,time
import numpy as np
whitelist1='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
whitelist_num='0123456789'
whitelist_eng='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def recognize():
    print('')
    position,img=cut('output_crop.png')
    hImg, wImg=img.shape
    pytesseract.pytesseract.tesseract_cmd=r'tesseract'
    position=position[1:]
    t1=time.monotonic()
    result=[]
    print(position)
    for i in range(len(position)+1):
        k=1
        # print(position[i])
        if i==0:
            k=img[0:hImg,3:position[i]]
        elif i==len(position):
            k=img[0:hImg,position[i-1]:]
        else:
            k=img[0:hImg,position[i-1]:position[i]]
        kernel = np.ones((3,3), np.uint8)
        
        k = cv2.dilate(k, kernel, iterations = 1)
        # cv2.imshow('ero',k)
        # cv2.waitKey(0)
        k = cv2.erode(k, kernel, iterations = 3)
        # cv2.imshow('ero',k)
        # cv2.waitKey(0)
        
        k = cv2.dilate(k, kernel, iterations = 1)
        # cv2.imshow('ero',k)
        # cv2.waitKey(0)
        
        k= np.pad(k, ((2, 2), (20, 20)), 'constant', constant_values=(255, 255))
        # cv2.imshow('a',k)
        # cv2.waitKey(0)
        # cv2.imwrite('a.png',k)
        
        result.append(pytesseract.image_to_string(k,lang='eng',config =f'--oem 1 --psm 10 -c tessedit_char_whitelist={whitelist1}').replace('\n',''))
        
    
    print(result)
    print("執行時間：",time.monotonic()-t1)
    # exit(0)
    t1=time.monotonic()
    def get_data(whitelist,img,x_start,x_end):
        boxes = pytesseract.image_to_boxes (img[0:hImg,x_start:x_end],lang='eng',config =f'--oem 3 --psm 8 -c tessedit_char_whitelist={whitelist}')
        temp=[]
        for k in boxes.splitlines():
            temp.append(k.split(' ')[0])
        # cv2.rectangle(img,(x_start, 0),(x_start, hImg), (0, 0, 255), 2)
        # cv2.waitKey(0)
        return temp

    left=[]

    boxes = pytesseract.image_to_boxes (img,lang='eng',config =f'--oem 3 --psm 8 -c tessedit_char_whitelist={whitelist1}')
    for b in boxes.splitlines():
        b= b.split(' ')
        print(b)
        x, y, w, h= int (b[1]), int (b[2]), int (b[3]) ,int(b[4])
        cv2.rectangle(img,(x, hImg-y),(w, hImg-h), (0, 0, 255), 2)
        left.append(b[0])
        
        # if '-' in b:
        #     if (w+x)/2<wImg/2: #左邊是英文字母
        #         print(1)
        #         # cv2.imshow('2',img[0:hImg,w:wImg])
        #         # print('左邊：',get_data(whitelist_eng,img,0,x))
        #         print('左邊:',left[:-1])
        #         print('右邊：',get_data(whitelist_num,img,w,wImg))
        #         # break
        #     else:# 左邊是數字
        #         print(2)
        #         # cv2.imshow('2',img[0:hImg,w:wImg])
        #         # print('左邊：',get_data(whitelist_num,img,0,x))
        #         print('左邊:',left[:-1])
        #         print('右邊：',get_data(whitelist_eng,img,w,wImg))
        #         # break
    # print(left)
    # print(''.join(left))
    print("執行時間：",time.monotonic()-t1)
    return ''.join(left)
    


