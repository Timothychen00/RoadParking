import multiprocessing
from yolov4.detect import main
import time


if __name__=='__main__':#這邊會需要這個是為了阻止runtime err，因為python禁止在子進程裡面重新創建進程。而進程的創建方式就相當於將主進程copy一份，才能匯入所有的依賴
    print('Start')
    ts=time.monotonic()
    p_list=[]
    p1=multiprocessing.Process(target=main,args=('yolov4/data/images/capture.jpg',))
    p2=multiprocessing.Process(target=main,args=('yolov4/data/images/capture.jpg',))
    p3=multiprocessing.Process(target=main,args=('yolov4/data/images/capture.jpg',))
    p4=multiprocessing.Process(target=main,args=('yolov4/data/images/capture.jpg',))

    p_list.append(p1)
    p_list.append(p2)
    p_list.append(p3)
    p_list.append(p4)

    for p in p_list:
        p.start()
    
    # 調整多程順序
    for p in p_list:
        p.join()
        
    te=time.monotonic()
    print(te-ts)
    ts=time.monotonic()
    main('yolov4/data/images/capture.jpg')
    main('yolov4/data/images/capture.jpg')
    main('yolov4/data/images/capture.jpg')
    main('yolov4/data/images/capture.jpg')
    te=time.monotonic()
    print(te-ts)
    
    