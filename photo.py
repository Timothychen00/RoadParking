
import aiohttp,aiofiles,asyncio,time,async_timeout,json
from mqtt_send import send
from network_scan import update_ip
import yolov4.detect
import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from threading import Thread
import testtt

devices={'8:B6:1F:39:B2:FC':["0.0.0.0","lost"],'44:17:93:7E:3B:7C':["192.168.92.35","lost"],'8:B6:1F:39:AF:20':['0.0.0.0','lost']}
# devices=update_ip(devices)
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
    print('[MAIN-PROCESS]',devices_color[name],'get_photo:',name,ip,bcolors.ENDC)
    for i in devices:
        devices[i][1]="lost"
    try:
        # print(name)
        async with async_timeout.timeout(2):
            async with aiohttp.ClientSession() as session:
                async with session.get("http://"+ip+"/capture?") as resp:
                    # print(resp.headers['Content-Type'])

                    if resp.status == 200:
                        devices[name][1]="alive"
                        # print(devices[name][1])
                        if resp.headers['Content-Type']=="image/jpeg":
                            f = await aiofiles.open("output/"+str(name)+".jpeg", mode='wb')
                            await f.write(await resp.read())
                            await f.close()
                            print('[MAIN-PROCESS]',devices_color[name],'get_photo',name,'done',bcolors.ENDC,'image')
                            return ['image','',name]
                        else:
                            return ['text',await resp.read(),name]
    except:
        if name=='44:17:93:7E:3B:7C':
            print('fuck')
            asyncio.sleep(2)
        print('[MAIN-PROCESS]',devices_color[name],'get_photo',name,'done',bcolors.ENDC,'err')
        return ['err','',name]
    
def image_callback(result):# input for a dict(result,mac)
    print('\t[SUB-PROCESS] recognize result:',result)
    err=[]
    if result['str']:
        if len(result['str'])<=7:
            err.append('length_error')
        if '-' not in result['str']:
            err.append('pattern_error')
    else:
        err.append('non_return')
    
    print('\t[SUB-PROCESS] recognize error:',result)
    if len(err)>0: #有錯誤的發生
        #錯誤處理
        msg=[{'mac':result['mac']},{'error':err}]
    else:
        msg=[{'mac':result['mac']},{'license_plate':result['str'],'status':'inuse'}]
        
    print('\t[SUB-PROCESS] Parking image type send:',result)
    send(msg,'Parking')# update parking errors

    # print('recognized:',input)
    
async def main():
    # 建立 Task 列表
    tasks = []
    for i in devices:
        task=asyncio.create_task(get_photo(devices[i][0],i))
        # task.add_done_callback(print(task.result))
        tasks.append(task)

    for k in tasks:
        await k
        result=k.result()# if get one ->do one
        print('\t\033[93m[SUB-PROCESS] task_result',result,'\033[0m')
        if result[0]=='image':
            # print('fuck')
            Pool.apply_async(yolov4.detect.main,args=('output/'+result[2]+'.jpeg',),callback=print,error_callback=print)
            Pool.apply_async(testtt.recognize,args=(result[2],),callback=image_callback,error_callback=print)
        elif result[0]=='text':
            if result[1]=='There\'s a car inside':#inuse
                msg=[{'mac':result['mac']},{'status':'inuse'}]
            else:#empty
                msg=[{'mac':result['mac']},{'status':'empty'}]
                
    return            #need to process


if __name__=='__main__':# main time loop
    print('updated:\n',devices)
    Pool=multiprocessing.Pool(processes=1)
    
    ts=0
    while True:
        te=time.monotonic()
        if te-ts>20 or ts==0:
            print('[MAIN-PROCESS]-'*20)
            result=asyncio.run(main())
            
            msg=[]
            for i in devices:
                msg.append([{"mac":i},{"status":devices[i][1]}])
            print('[MAIN-PROCESS] send:',msg)
            msg=json.dumps(msg)
            send(msg)# send to mqtt
            ts=te
