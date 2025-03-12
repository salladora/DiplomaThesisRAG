import re
import boto3
import os
from config import dotenv_path, bucket_name
from dotenv import load_dotenv
load_dotenv(dotenv_path)


s3 = boto3.client('s3')

# bucket and folder names
bucket_name = "wiim-rag"
source_folder = r""
destination_folder = source_folder



def download_file_from_s3(bucket, key):
    file_path = '/'.join(key.split('/')[1:]) #takey s3 key without bucket
    temp_file_path = f"tmp/{file_path}"  # temporary storage for processing
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    s3.download_file(bucket, key, temp_file_path)
    return file_path



# parses all docs in temporary storage and uploads them as individual docs to s3
def remove_metadata_from_s3():
    try:
        # lists all objects in source folder
        file_list = s3.list_objects_v2(Bucket=bucket_name, Prefix=source_folder)
        if 'Contents' not in file_list:
            print(f"No files found in S3 folder '{source_folder}'.")
            return

        for obj in file_list['Contents']:
            file_key = obj['Key']
           

            # downloads file to parse and stores S3 directory structure
            file_name = download_file_from_s3(bucket_name, file_key)
            local_file_path = f"tmp/{file_name}"

            try:
                with open(local_file_path, "r") as file:
                    content = file.read()

                # Remove all metadata blocks (pattern assumes key-value pairs)
                firstStepCleaned = re.sub(r'Document\(id_=.*?text=\'', '', content, flags=re.DOTALL)
                secondStepCleaned = re.sub(r"', path=.*?}'\)", '', firstStepCleaned, flags=re.DOTALL)
                # Prepare parsed content for upload
                upload_key = f"{destination_folder}/{file_name.split('.')[0]}.txt"
                document_text = secondStepCleaned

                # Upload parsed content back to S3
                s3.put_object(
                    Bucket=bucket_name,
                    Key=upload_key,
                    Body=document_text
                )
                print(f"Cleaned document uploaded as: {upload_key}")
            finally:
                # cleans up temporary file
                if os.path.exists(local_file_path):
                    os.remove(local_file_path)
                    print(f"Temporary file deleted: {local_file_path}")    
    except Exception as e:
        print(f"Error occurred while processing files from S3: {e}")

remove_metadata_from_s3()






















