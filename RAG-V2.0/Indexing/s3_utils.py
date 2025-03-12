import os
import boto3

s3 = boto3.client('s3')

def list_s3_files(bucket_name: str, folder: str) -> list:
    """Fetches a list of files from an S3 folder."""
    try:
        file_list = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder)
        return [obj['Key'] for obj in file_list.get('Contents', []) if not obj['Key'].endswith('/')]
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def download_file_from_s3(bucket: str, key: str) -> str:
    """Downloads file from S3 to a temporary location."""
    temp_file_path = f"tmp/{key}"
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    s3.download_file(bucket, key, temp_file_path)
    return key