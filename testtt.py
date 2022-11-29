import cv2
import pytesseract
from separate import cut
import sys,time
whitelist1='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
whitelist_num='0123456789'
whitelist_eng='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

position,img=cut('output/capture(9)-cut.png')
cv2.imshow('origin',img)
cv2.waitKey(0)


hImg, wImg=img.shape
pytesseract.pytesseract.tesseract_cmd=r'tesseract'


t1=time.monotonic()

for i in range(len(position)):
    if i==1:
        cv2.imshow('a',img[0:hImg,0:position[i]])
        cv2.waitKey(0)
        print(pytesseract.image_to_string(img[0:hImg,0:position[i]],lang='eng',config =f'--oem 3 --psm 8 -c tessedit_char_whitelist={whitelist_eng}'))




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
    
    if '-' in b:
        if (w+x)/2<wImg/2: #左邊是英文字母
            print(1)
            # cv2.imshow('2',img[0:hImg,w:wImg])
            # print('左邊：',get_data(whitelist_eng,img,0,x))
            print('左邊:',left[:-1])
            print('右邊：',get_data(whitelist_num,img,w,wImg))
            break
        else:# 左邊是數字
            print(2)
            # cv2.imshow('2',img[0:hImg,w:wImg])
            # print('左邊：',get_data(whitelist_num,img,0,x))
            print('左邊:',left[:-1])
            print('右邊：',get_data(whitelist_eng,img,w,wImg))
            break

print("執行時間：",time.monotonic()-t1)
cv2.imshow("img",img)
cv2.waitKey(0)


