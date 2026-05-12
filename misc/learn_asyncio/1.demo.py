import asyncio
import time


def sync_function(test_param: str) -> str:
    print("This is a synchronous function")
    
    time.sleep(0.1)
    
    return f"Sync results: {test_param}"

# coroutine function - basically they are functions but their execution can be paused
async def async_function(test_param: str) -> str:
    print("This is a asynchronous function")
    
    asyncio.sleep(0.1)
    
    return f"Async results: {test_param}"  


async def main():
    # sync_results = sync_function("Test")
    # print(sync_results)     
    
    # coroutine_obj = async_function("Test")
    # print("coroutine_obj - ", coroutine_obj)
    
    # coroutine_result = await coroutine_obj
    # print("coroutine_result - ", coroutine_result)
    
    task = asyncio.create_task(async_function('Test'))
    print(task)
    
    task_result = await task
    print(task_result)
    
if __name__ == '__main__':
    asyncio.run(main())