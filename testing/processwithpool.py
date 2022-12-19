# 导入相关multiprocessing包
import multiprocessing
from yolov4.detect import main
import time
# 创建拥有CPU核心数量的进程的进程池
if __name__=='__main__':
    pool = multiprocessing.Pool(processes=4)
    ts=time.monotonic()
        # # 阻塞等待当前任务的进程结束
        # pool.apply(func=pow, args=(i,2))

        # 不阻塞等待当前任务的进程结束
    for i in range(4):
        pool.apply_async(func=main, args=('yolov4/data/images/capture.jpg',))

    # # map函数到一个列表，阻塞等待返回值
    # results = pool.map(func=print, iterable=)

    # # 不阻塞等待返回值，未运行完就调用results会报错。
    # results = pool.map_async(func=print, iterable=[1])
    # print(results)
    te=time.monotonic()
    print(te-ts)
    # close后不会有新的进程加入到pool
    pool.close()

    # join函数等待所有子进程结束 # 调用join之前，先调用close函数，否则会出错。
    pool.join()
    te=time.monotonic()
    print(te-ts)

    # # 结束工作进程，不再处理未完成的任务。
    # pool.terminate()