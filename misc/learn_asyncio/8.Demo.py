# import time


# def read_file_sync(filepath):
#     with open(filepath, 'r') as file:
#         return file.read()

# def read_all_sync(filepaths):
#     return [read_file_sync(filepath) for filepath in filepaths]

# filepaths = ['file1.txt', 'file2.txt']


# start_time = time.time()
# data = read_all_sync(filepaths)
# print(f"Done in {time.time() - start_time} seconds")



import asyncio
import aiofiles

# Asynchronously reading a single file
async def read_file_async(filepath):
    async with aiofiles.open(filepath, 'r') as file:
        return await file.read()

async def read_all_async(filepaths):
    tasks = [read_file_async(filepath) for filepath in filepaths]
    return await asyncio.gather(*tasks)

# Running the async function
async def main():
    filepaths = ['file1.txt', 'file2.txt']
    data = await read_all_async(filepaths)
    print(data)

asyncio.run(main())



