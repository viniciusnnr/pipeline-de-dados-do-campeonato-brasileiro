import boto3
import os

def upload_to_s3(local_path: str, bucket: str, s3_key: str):
    if not os.path.exists(local_path):
        raise FileNotFoundError(local_path)

    s3 = boto3.client("s3")
    s3.upload_file(local_path, bucket, s3_key)
