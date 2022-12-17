
import aiohttp,aiofiles,asyncio,time,async_timeout,json
from mqtt_send import send
from network_scan import update_ip

devices={'8:B6:1F:39:B2:FC':["0.0.0.0","lost"],'44:17:93:7E:3B:7C':["0.0.0.0","lost"],'8:B6:1F:39:AF:20':['0.0.0.0','lost']}
devices=update_ip(devices)
print('updated:\n',devices)


async def get_photo(ip,name):
    global devices
    for i in devices:
        devices[i][1]="lost"
    try:
        print(name)
        async with async_timeout.timeout(2):
            async with aiohttp.ClientSession() as session:
                async with session.get("http://"+ip+"/check") as resp:
                    print(resp.headers['Content-Type'])

                    if resp.status == 200:
                        devices[name][1]="alive"
                        print(devices[name][1])
                        if resp.headers['Content-Type']=="image/jpeg":
                            f = await aiofiles.open("output/"+str(name)+".jpeg", mode='wb')
                            await f.write(await resp.read())
                            await f.close()
                        else:
                            pass
        return 'hh2'
    except:
        return 'hh'

async def main():
    # 建立 Task 列表
    tasks = []
    for i in devices:
        task=asyncio.create_task(get_photo(devices[i][0],i))
        # task.add_done_callback(print(task.result))
        tasks.append(task)
        
        
    for k in tasks:
        await k
        print(k.result())

        
        # 執行所有 Tasks

    # 輸出結果

    try:
        await asyncio.wait(tasks, timeout=2)
    except TimeoutError:
        print('The task was cancelled due to a timeout')


ts=0
while True:
    te=time.monotonic()
    if te-ts>1 or ts==0:
        asyncio.run(main())

        msg=[]
        for i in devices:
            msg.append([{"mac":i},{"status":devices[i][1]}])
        print(msg)
        msg=json.dumps(msg)
        send(msg)# send to mqtt
        ts=te

