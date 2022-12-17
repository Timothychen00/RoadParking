
import aiohttp,aiofiles,asyncio,time,async_timeout,json
from mqtt_send import send
from network_scan import update_ip
import yolov4.detect
import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from threading import Thread
import testtt


devices={'8:B6:1F:39:B2:FC':["0.0.0.0","lost"],'44:17:93:7E:3B:7C':["0.0.0.0","lost"],'8:B6:1F:39:AF:20':['0.0.0.0','lost']}
devices=update_ip(devices)
print('updated:\n',devices)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

devices_color={
    '8:B6:1F:39:B2:FC':bcolors.OKGREEN,#1
    '44:17:93:7E:3B:7C':bcolors.OKCYAN,#2
    '8:B6:1F:39:AF:20':bcolors.OKBLUE#3
}
async def get_photo(ip,name):
    global devices
    print(devices_color[name],'get_photo:',name,ip,bcolors.ENDC)
    for i in devices:
        devices[i][1]="lost"
    try:
        # print(name)
        async with async_timeout.timeout(2):
            async with aiohttp.ClientSession() as session:
                async with session.get("http://"+ip+"/check") as resp:
                    # print(resp.headers['Content-Type'])

                    if resp.status == 200:
                        devices[name][1]="alive"
                        # print(devices[name][1])
                        if resp.headers['Content-Type']=="image/jpeg":
                            f = await aiofiles.open("output/"+str(name)+".jpeg", mode='wb')
                            await f.write(await resp.read())
                            await f.close()
                            return ['image','',name]
                        else:
                            return ['text',await resp.read(),name]
    except:
        print(devices_color[name],'get_photo',name,'done',bcolors.ENDC)
        return ['err','',name]

async def main():
    # 建立 Task 列表
    tasks = []
    for i in devices:
        task=asyncio.create_task(get_photo(devices[i][0],i))
        # task.add_done_callback(print(task.result))
        tasks.append(task)
        
    images=[]
    for k in tasks:
        await k
        result=k.result()
        if result[0]=='image':
            images.append(result[2])
        elif result[0]=='text':
            if result[1]=='There\'s a car inside':
                
            #update text
            pass
                
        print(k.result())
    return images           #need to process


        
        # 執行所有 Tasks

    # 輸出結果

if __name__=='__main__':# main time loop
    Pool=multiprocessing.Pool(processes=1)
    
    ts=0
    while True:
        te=time.monotonic()
        if te-ts>1 or ts==0:
            result=asyncio.run(main())
            print(result)
            Pool.apply_async(yolov4.detect.main,args=('yolov4/data/images/capture.jpg'),callback=print('fuck'))
            msg=[]
            for i in devices:
                msg.append([{"mac":i},{"status":devices[i][1]}])
            print(msg)
            msg=json.dumps(msg)
            send(msg)# send to mqtt
            ts=te
