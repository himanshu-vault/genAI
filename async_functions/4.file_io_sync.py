# Synchronously reading multiple files
def read_file_sync(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def read_all_sync(filepaths):
    return [read_file_sync(filepath) for filepath in filepaths]

filepaths = ['C:\\Users\\himan\\OneDrive\\genAI\\async_functions\\file1.txt', 'C:\\Users\\himan\\OneDrive\\genAI\\async_functions\\file2.txt']
data = read_all_sync(filepaths)
print(data)