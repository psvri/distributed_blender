from utils.storage_utils import StorageUtils
from utils.image_utils import ImageSticher
import os
import sys

if __name__ == "__main__":

    blend_file = sys.argv[1]
    render_output_folder = sys.argv[2]
    bucket_folder = blend_file.replace('.blend','_render')

    storage_utils = StorageUtils(
        access_key = os.environ['access_key'],
        secret_key = os.environ['secret_key'],
        region_name = os.environ['region_name'],
        endpoint_url = os.environ['endpoint_url'],
        bucket_name = os.environ['bucket_name']
    )

    storage_utils.get_data_in_folder(bucket_folder, render_output_folder)

    sticher = ImageSticher()
    sticher.sticher(os.path.join(render_output_folder, bucket_folder))