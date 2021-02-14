from utils.storage_utils import StorageUtils
from utils.queue_utils import TaskQueue
import collections
import subprocess
import os

def task(queue_message):
    message = Message(*queue_message.decode("utf-8").split( ))
    print(message)
    storage_utils.get_data(message.blend_file)
    subprocess.run([
        'blender',
        '-b', 
        message.blend_file, 
        '-E', 
        'CYCLES',
        '-P',
        'border_render.py',
        '--', 
        message.min_x,
        message.max_x,
        message.min_y,
        message.max_y,
        message.frame_number
    ])
    bucket_path = message.blend_file.replace('.blend','')+'_render/'+message.frame_number+'/'+f'{message.min_x}_{message.max_x}_{message.min_y}_{message.max_y}.png'
    storage_utils.put_data('br.png', bucket_path)


storage_utils = StorageUtils(
    access_key = os.environ['access_key'],
    secret_key = os.environ['secret_key'],
    region_name = os.environ['region_name'],
    endpoint_url = os.environ['endpoint_url'],
    bucket_name = os.environ['bucket_name']
)

Message = collections.namedtuple('Message', 'blend_file frame_number min_x max_x min_y max_y') 

taskfetcher = TaskQueue(
    os.environ['amqp_url']
)

while taskfetcher.get_queue_length() != 0:
    taskfetcher.perform_task(task)

taskfetcher.close()