import cv2,sys,time
import numpy
import matplotlib.pyplot as plt

path='output.png'
def cut(path):
    image= cv2. imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    # cv2.imshow('',image)
    # cv2.waitKey(0)
    image=cv2.GaussianBlur(image,(5,5),10)
    # cv2.imshow('1',image)
    # cv2.waitKey(0)
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)


    print(image)
    # cv2.imshow('origin_image',image)
    # cv2.waitKey(0)
    # 圖片的座標是y，x
    height=image.shape[0]
    width=image.shape[1]
    print(image)

    white_point_y=numpy.count_nonzero(image ==255, axis=1)
    white_max_y=white_point_y.max()

    temp=[0,0]
    #垂直切y
    for i in range(len(white_point_y)):
        if white_point_y[i]>white_max_y*0.7 and( i>5 or i< height-5):
            if i<=len(image)/2:
                temp[0]=i-15
            else:
                temp[1]=i+15
                break

        
    image_color = cv2.imread(path, cv2.IMREAD_COLOR)
    print('temp',temp)


    # cv2.line(image_color, (0,temp[0]), (width,temp[0]), (0, 0, 255),1)
    # cv2.line(image_color, (0,temp[1]), (width,temp[1]), (0, 0, 255),1)

    #切割
    image_color=image_color[temp[0]+1:temp[1]]
    image_binary=image[temp[0]+1:temp[1]]

    # cv2.imshow('image_colors',image_color)
    # cv2.waitKey(0)


    height=image_binary.shape[0]
    width=image_binary.shape[1]
    white_point_x=numpy.count_nonzero(image_binary ==255, axis=0)
    white_max_x=white_point_x.max()
    black_point_x=numpy.count_nonzero(image_binary ==0, axis=0)
    black_min_x=numpy.min(black_point_x)
    #初始值
    if black_min_x==0:
        black_min_x=5 


    temp_x=[0]*width
    temp_x_position=[0]
    times=0
    print(width/8)
    for i in range(0,len(black_point_x)):
        if black_point_x[i]<black_min_x :
            if times>=1:
                print(i,temp_x_position[times])
                if i-temp_x_position[times]>width/8 :
                    temp_x[i]=i
                    temp_x_position.append(i)
                    times+=1
            else:
                temp_x_position.append(i)
                times+=1
            
    print('tempx:',temp_x)
    print('tempx_position',temp_x_position)

    # # line (x,y)
    # for i in temp_x_position[1:]:
    #     print(i)
    #     cv2.line(image_color, (i,0), (i,height), (0, 0, 255),1)

    value = numpy.array(white_point_x)
    label = numpy.array(range(len(white_point_x)))
    valueb = numpy.array(black_point_x)
    labelb = numpy.array(range(len(black_point_x)))
    print()
    # print(white_point_x)
    # plt.bar(label, value)
    # plt.show()
    # plt.bar(labelb, valueb)
    # plt.show()
    # cv2.imshow('213123',image_color)
    # cv2.waitKey(0)
    # cv2.imwrite('output2.png', image_binary)


    return temp_x_position,image_binary















    # def capture(y_min,y_max,x_min,x_max,img):
    #     cv2.imshow('',image_binary)
    #     cv2.waitKey(0)
    #     # print(y_min,y_max,x_min,x_max)
    #     tempy=img[y_min:y_max+1]
    #     tempx=numpy.array([])
    #     for i in tempy:
    #         temp=numpy.array(i[x_min:x_max+1])
    #         tempx=numpy.append(tempx,temp)
    #         # print(temp)
            
    #     # print('',tempx,tempx.shape)
    #     tempx=numpy.reshape(tempx,(x_max-x_min+1,y_max-y_min))
    #     # print(tempx)
    #     # print(type(tempx))
    #     # print(type(tempx.shape))
    #     cv2.imshow('1',tempx)
    #     cv2.waitKey(0)
        
    # for i in range(len(temp_x_position[1:])):
    #     capture(0,height,temp_x_position[i],temp_x_position[i+1],image_binary)