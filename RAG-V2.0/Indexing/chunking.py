import os
from s3_utils import download_file_from_s3
from llama_index.core.node_parser.text import TokenTextSplitter
from config import chunk_size, chunk_overlap

def chunking_from_s3(bucket: str, key: str) -> dict:
    """Splits downloaded document into chunks."""
    download_file_from_s3(bucket, key)
    local_file_path = f"tmp/{key}"
    try:
        with open(local_file_path, 'r', encoding="utf-8") as file:
            chunker = TokenTextSplitter.from_defaults(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunks = chunker.split_text_metadata_aware(file.read(), key)
    except Exception as e:
        print(f"Error while chunking: {e}")
        return {}
    finally:
        os.remove(local_file_path)

    return {'chunks': chunks, 'fileName': key}
