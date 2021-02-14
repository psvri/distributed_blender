from utils.queue_utils import TaskQueue
from utils.storage_utils import StorageUtils
import os
import sys

def create_task_per_frame(file_name, frame_number, task_queue, step=0.1):
    min_x = 0
    max_x = min_x + step
    min_y = 0
    max_y = min_y + step
    while max_y <= 1 :
        prev_min_x = min_x
        prev_max_x = max_x
        while max_x <= 1:
            message  = f"{file_name} {frame_number} {round(min_x,2)} {round(max_x,2)} {round(min_y,2)} {round(max_y,2)}"
            print(message)
            task_queue.publish_message(message)
            min_x = min_x + step
            max_x = max_x + step
        min_x = prev_min_x
        max_x = prev_max_x
        min_y = min_y + step
        max_y = max_y + step

if __name__ == "__main__":
    amqp_url = os.environ['amqp_url']

    task_queue = TaskQueue(amqp_url)

    file_path = sys.argv[1]
    file_name = os.path.basename(file_path)
    frame_start = int(sys.argv[2])
    frame_end = int(sys.argv[3])
    step = float(sys.argv[4])

    storage_utils = StorageUtils(
        access_key = os.environ['access_key'],
        secret_key = os.environ['secret_key'],
        region_name = os.environ['region_name'],
        endpoint_url = os.environ['endpoint_url'],
        bucket_name = os.environ['bucket_name']
    )

    storage_utils.put_data(file_path, file_name)

    for frame_number in range(frame_start, frame_end+1):
        create_task_per_frame(file_name, frame_number, task_queue, step)

    task_queue.close()