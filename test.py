
import cv2
import numpy
image = cv2.imread('test.png', cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 11, 1)

print(image[0])

print(len(image),len(image[0]))
def capture(y_min,y_max,x_min,x_max,img):
    tempy=img[y_min:y_max+1]
    tempx=numpy.array([])
    for i in tempy:
        temp=numpy.array(i[x_min:x_max+1])
        tempx=numpy.append(tempx,temp)
        print(temp)
    print(numpy.reshape(tempx,(y_max-y_min+1,x_max-x_min+1)))
    cv2.imshow('1',numpy.reshape(tempx,(y_max-y_min+1,x_max-x_min+1)))
    cv2.waitKey(0)
capture(5,10,5,10,image)
# with open('test.txt','w') as f1:
#     for i in tempx:
#         f1.writelines(str(i)+"\n")

