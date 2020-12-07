import os
import time

while True:
    try:
        list_dir = os.listdir('/data')    
        print('dir contents:')
        for entry in list_dir:
            print(entry)
    except OSError as e:
        print('listdir error: {}'.format(e))

    time.sleep(60)
