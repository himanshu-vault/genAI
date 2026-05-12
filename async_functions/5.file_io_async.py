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
    filepaths = ['C:\\Users\\himan\\OneDrive\\genAI\\async_functions\\file1.txt', 'C:\\Users\\himan\\OneDrive\\genAI\\async_functions\\file2.txt']
    data = await read_all_async(filepaths)
    print(data)

asyncio.run(main())
