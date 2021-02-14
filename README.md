
# distributed_blender
Distributed rendering for blender using docker containers.

# Overview

At an high level the projcet uses an S3 compatible object store to hold the blend file (the blend file should include the data as well) .

RabbitMQ is used as an message queue to hold tasks to be done by the containers. The task message is of format 
```
<blend_file> <frame_number> <min_x> <max_x> <min_y> <max_y>
```
where
- blend_file is the blend file in the object store to be rendered
- frame number is the frame to be rendered
- min_x, max_x & min_y,max_y are the regions of the frame to be rendered 


The containers pick a message form the queue, render a portion of the frame as mentioned in the queue message and upload them back to the object store under the folder <blend_file>\_rendered/<frame_number>/<min_x>\_<max_x>\_<min_y>\_<max_y>.png. The containers keep running until there are no more messages in the queue.

### To create a task in the queue use 
```
python3 task_creator.py <path_to_blend_file> <frame_start> <frame_end> <step_size>
```
Which uploads your blend file and publishes the task messages to the queue . The step size above must be between 0 to 1 which controls the size of region which will be rendered.

### To stitch the portions of frame images use 
```
python3 image_merger.py <blend_file_name> <render_output_folder_path>
```
Which downloads the rendered images , merges them and places them in render_output_folder_path/merged/


### To build the docker image use
```
docker build -t <image_name>
```

### To run the docker image use
```
docker run --env_file <environment_file> <image_name>
```

To run any of the above scripts and the container please ensure that the following environment variables are set
| environment variable | description |
| ------ | ------ |
| access_key | access id of the s3 bucket |
| secret_key | secret key of the s3 bucket |
| region_name | s3 bucket region |
| endpoint_url | s3 bucket endpoint URL |
| bucket_name | s3 bucket name |
| amqp_url | message queue URL |

