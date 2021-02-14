import boto3
import os

class StorageUtils:

    def __init__(self, access_key, secret_key, region_name, endpoint_url, bucket_name):
        s3 = boto3.resource(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name,
            endpoint_url=endpoint_url
        )
        self.storage_handler = s3.Bucket('test-bucket')

    def put_data(self, input_filename, bucket_filename):
        self.storage_handler.upload_file(input_filename, bucket_filename)

    def get_data(self, filename):
        self.storage_handler.download_file(filename,filename)

    def get_data_in_folder(self, foldername, destination_folder):
        objects = self.storage_handler.objects.filter(Prefix=foldername)
        for obj in objects:      
            file_path, filename = os.path.split(obj.key)
            file_path = os.path.join(destination_folder, file_path)
            destination_path = os.path.join(destination_folder, obj.key)
            os.makedirs(file_path, exist_ok=True)
            if(os.path.exists(destination_path)):
                os.remove(destination_path)
            self.storage_handler.download_file(obj.key, destination_path)
        