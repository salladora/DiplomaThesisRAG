from config import s3_bucket_name, source_folder, pc_api, pc_index_name
from s3_utils import list_s3_files
from chunking import chunking_from_s3
from embedding import embedding, list_vectors_with_metadata
from upload import upload_to_pinecone
from pinecone import Pinecone  

pc = Pinecone(api_key=pc_api)
index = pc.Index(pc_index_name)

def process_files():
    """Main pipeline: List files, chunk, embed, and upload."""
    file_keys = list_s3_files(s3_bucket_name, source_folder)
    if not file_keys:
        print("No files found.")
        return
    
    for doc_id, file_key in enumerate(file_keys, start=1):
        print(f"Processing {file_key}...")
        chunks_and_names = chunking_from_s3(s3_bucket_name, file_key)
        if not chunks_and_names:
            continue
        
        chunks = chunks_and_names['chunks']
        file_name = chunks_and_names['fileName']
        embeddings = embedding(chunks)
        vectors_with_metadata = list_vectors_with_metadata(embeddings, chunks, file_name, doc_id)
        upload_to_pinecone(index, vectors_with_metadata)

# Run the pipeline
process_files()

# parsedFinal/Projekt/
