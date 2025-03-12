from config import namespace, upload_batch_size

def upload_to_pinecone(index, vectors_with_metadata: list):
    """Uploads embeddings to Pinecone in batches."""
    if not vectors_with_metadata:
        print("No vectors to upload.")
        return

    try:
        for batch_start in range(0, len(vectors_with_metadata), upload_batch_size):
            batch = vectors_with_metadata[batch_start:batch_start + upload_batch_size]
            index.upsert(vectors=batch, namespace=namespace)
            print(f"Uploaded batch {batch_start // upload_batch_size + 1} with {len(batch)} vectors.")
    except Exception as e:
        print(f"Error uploading to Pinecone: {e}")
