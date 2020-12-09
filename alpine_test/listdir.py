import os, sys
import time
import minio

# 
# Access environment vars
#

# Local k8s master test
# minio_access_key = os.environ['ACCESS_KEY']
# minio_secret_key = os.environ['SECRET_KEY']
# minio_url = 'localhost:9000'

# In-cluster vars
minio_access_key = os.environ['MINIO_ACCESS_KEY'].rstrip()
minio_secret_key = os.environ['MINIO_SECRET_KEY'].rstrip()
minio_url = 'minio-1607465410.minio.svc.cluster.local:9000'

# print(minio_access_key)
# print(minio_url)

def print_minio_write_result(res):
    msg_fmt = 'Created {:s}: etag = {}, version-id = {}'
    print(msg_fmt.format(res.object_name, res.etag, res.version_id))


client = minio.Minio(minio_url,
                     access_key=minio_access_key,
                     secret_key=minio_secret_key,
                     secure=False
)

buckets = client.list_buckets()
for b in buckets:
    print(b.name, b.creation_date)

objs = client.list_objects('data')
for o in objs:
    print(o.object_name, o.size)

# # Test write file
res = client.fput_object('data', 
                         'listdir.py',
                         '/app/listdir.py'
)
print_minio_write_result(res)

# sys.exit(0)

while True:
    try:
        list_dir = os.listdir('/data')    
        print('dir contents:')
        for entry in list_dir:
            print(entry)
    except OSError as e:
        print('listdir error: {}'.format(e))

    time.sleep(60)
