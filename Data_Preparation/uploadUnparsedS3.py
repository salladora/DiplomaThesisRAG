import boto3
import os
from config import dotenv_path, bucket_name
from dotenv import load_dotenv
load_dotenv(dotenv_path)
s3 = boto3.client('s3')

# defines variables
bucket_name = bucket_name
local_source_folder = r"" #local folder to be uploaded
s3_destination_folder = ""
file_types = [".pdf", ".docx", ".txt"]

#upload function
def upload_folder_to_s3(local_folder, bucket_name, s3_folder, allowed_file_types):
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            # checks file extension
            if os.path.splitext(file)[1].lower() in allowed_file_types:
                local_file_path_windows = os.path.join(root, file)
                local_file_path = local_file_path_windows.replace("\\", "/")
                
                # contructs s3 path analog to local path
                relative_path = os.path.relpath(local_file_path, local_folder)
                s3_file_path = os.path.join(s3_folder, relative_path)

                # uploads file
                print(f"Uploading {relative_path} to s3://{bucket_name}/{s3_file_path}...")
                s3.upload_file(local_file_path, bucket_name, s3_file_path)
            else:
                print(f"Skipping {file}: Unsupported file type.")
    print("Upload complete.")

upload_folder_to_s3(local_source_folder, bucket_name, s3_destination_folder, file_types)
