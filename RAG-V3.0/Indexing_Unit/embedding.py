from config import open_ai_api
from openai import OpenAI  

client = OpenAI(api_key=open_ai_api)

def embedding(chunks: list) -> list:
    """Embeds text chunks."""
    embeddings = []
    for chunk in chunks:
        try:
            response = client.embeddings.create(model="text-embedding-3-large", input=chunk)
            embeddings.append(response.data[0].embedding)
        except Exception as e:
            print(f"Error embedding chunk: {e}")
    return embeddings

def list_vectors_with_metadata(vectors: list, chunks: list, file_name: str, doc_id: int) -> list:
    """ Creates a list of vector embeddings and their respective metadata.

    For each chunk a dictionary is created containing the index-id, the vector embedding, the plaintext chunk and the document name.
    The index-id is created in this method by adding a running number to add to each chunk of a document that gets added to the document id.
    A list is created that contains the dictionary of every chunk.

    Args:
        vectors : List of all vector embeddings
        plaintext : List of all plaintext chunks
        fileName : name of the document being processed
        doc_id : id of the document being processed

    Returns:
        vectorsWithMetadata : List of dictionaries with chunk-data
    """
    vectors_with_metadata = []
    for i, vector in enumerate(vectors):
        vec_id = f"{i}-{doc_id}-x"
        vectors_with_metadata.append({
            "id": vec_id,
            "values": vector,
            "metadata": {'text': chunks[i], 'name': file_name}
        })
    return vectors_with_metadata
