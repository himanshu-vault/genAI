import asyncio
import time

def sync_task():
    print("sync_task - Starting a slow sync task...")
    time.sleep(5)  # Simulating a long task
    print("sync_task - Finished the slow task.")

async def async_wrapper():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, sync_task)

async def say_hello_async():
    await asyncio.sleep(2)  # Simulates waiting for 2 seconds
    print("say_hello_async - Hello, Async World!")

async def do_something_else():
    print("do_something_else - Starting another task...")
    await asyncio.sleep(1)  # Simulates doing something else for 1 second
    print("do_something_else - Finished another task!")

async def main():
    await asyncio.gather(
        async_wrapper(),
        say_hello_async(),
        do_something_else()
        # Imagine other async tasks here
    )



start_time = time.time()
asyncio.run(main())
print(f"Done in {time.time() - start_time} seconds")