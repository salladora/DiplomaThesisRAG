import boto3
import os
from llama_parse import LlamaParse
from config import dotenv_path, bucket_name
from dotenv import load_dotenv
load_dotenv(dotenv_path)


s3 = boto3.client('s3')

# bucket and folder names
bucket_name = bucket_name
source_folder = r""
destination_folder = r""


# sets up parser
parser = LlamaParse(
    result_type="text"  # "markdown" and "text" are available
)

# maps file extensions to parsers
file_extractors = {
    ".pdf": parser,
    ".docx": parser,
    ".txt": parser,
}


def download_file_from_s3(bucket, key):
    file_path = '/'.join(key.split('/')[1:]) #takey s3 key without bucket
    temp_file_path = f"tmp/{file_path}"  # temporary storage for processing
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    s3.download_file(bucket, key, temp_file_path)
    return file_path


# parses all docs in temporary storage and uploads them as individual docs to s3
def parse_files_from_s3():
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
                # parses file
                file_extension = os.path.splitext(local_file_path)[1]
                extractor = file_extractors.get(file_extension)
                if extractor:
                    extra_info = {"file_name": file_name}

                    #automatically closes file after parsing
                    with open(local_file_path, 'rb') as file:
                        document_content = extractor.load_data(file, extra_info=extra_info)

                    # Prepare parsed content for upload
                    upload_key = f"{destination_folder}/{file_name.split('.')[0]}.txt"
                    document_text = str(document_content)

                    # Upload parsed content back to S3
                    s3.put_object(
                        Bucket=bucket_name,
                        Key=upload_key,
                        Body=document_text
                    )
                    print(f"Parsed document uploaded as: {upload_key}")
            finally:
                # cleans up temporary file
                if os.path.exists(local_file_path):
                    os.remove(local_file_path)
                    print(f"Temporary file deleted: {local_file_path}")    
    except Exception as e:
        print(f"Error occurred while processing files from S3: {e}")

parse_files_from_s3()