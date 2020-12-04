import os

list_dir = os.listdir('/data')
print('dir contents:')
for entry in list_dir:
    print(entry)
