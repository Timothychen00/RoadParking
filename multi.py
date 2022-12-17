import asyncio
from concurrent.futures import ProcessPoolExecutor


def run_loop_in_process():
    async def subprocess_async_work():
        await asyncio.sleep(5) #whatever async code you need
    asyncio.run(subprocess_async_work())

async def main():
    loop = asyncio.get_running_loop()
    pool = ProcessPoolExecutor()
    tasks = [loop.run_in_executor(pool, run_loop_in_process) for _ in range(5)]
    await asyncio.gather(*tasks)#等待其他的任務執行結束，如果沒有的話main就會先終結然後任務才會結束
    #可以用 result=await asyncio.gather(任務)等待所有的任務一次結束然後再一起獲得其值
    print(asyncio.Task(loop))
    

if __name__ == "__main__":
    asyncio.run(main())