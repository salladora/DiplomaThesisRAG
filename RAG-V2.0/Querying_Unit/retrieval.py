"""Retrieves chunks from Pinecone based on pre-processed query"""
from pinecone import Pinecone
import openai 
from openai import OpenAI
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.query_engine import RetrieverQueryEngine
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, OPENAI_API_KEY, PINECONE_NAMESPACE, top_k
from llama_index.embeddings.openai import OpenAIEmbedding

# Initializing Components
pc = Pinecone(api_key=PINECONE_API_KEY)
openai.api_key = OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
embedding_model = OpenAIEmbedding(model ="text-embedding-3-large")
index = pc.Index(PINECONE_INDEX_NAME)
vector_store = PineconeVectorStore(api_key=PINECONE_API_KEY,index_name= PINECONE_INDEX_NAME, namespace=PINECONE_NAMESPACE)
vector_index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embedding_model)
retriever = vector_index.as_retriever(similarity_top_k=top_k, namespace = PINECONE_NAMESPACE)
query_engine = RetrieverQueryEngine(retriever=retriever, response_synthesizer=None)


def retrieve_documents(subqueries: list) -> list:
    """ Retrieves relevant chunks from Pinecone based on pre-processed user query.
    
    Takes pre-processed subqueries and embedds them with text-embedding-3-large. Top k documents get identified for each subquery.
    Pinecones ANN-Search is based on cosine similiarity. The Metadata (inkluding chunk-text and document name) gets retrieved and added to the all_retrieved_chunks list.
    Before a new chunks gets added to the list, it gets checked if that chunk is already included, to avoid duplicates

    Args:
        subqueries : List of preprocessed Subqueries

    Returns:
        all_retrieved_chunks : List off contents of all retrieved chunks
    
    """
    all_retrieved_chunks = []
    seen_chunks = set()  

    try:
        for subquery in subqueries:
            retrieved_response = query_engine.query(subquery)
            print(f"this is the retrieved response: {retrieved_response}")

            if hasattr(retrieved_response, "source_nodes"):
                for node in retrieved_response.source_nodes:
                    doc_id = getattr(node.node, "node_id", None) 
                    if doc_id is None:
                        print(f"Warning: doc_id is NONE, node {node} is being hashed")
                        doc_id = hash(node.node.text)
                    if doc_id not in seen_chunks:
                        all_retrieved_chunks.append(node)
                        seen_chunks.add(doc_id)
            else:
                print("no source nodes found in repsonse")
    except Exception as e:  
        print(f"Error while retrieving documents: {e}")
        return []
    #print(all_retrieved_chunks)
    return all_retrieved_chunks  


# Test retrieval
if __name__ == "__main__":
    test_subqueries = [
        "what is albanias next unicorn?",
        "what are design dimensions of virtual collaborative learning?"
    ]
    
    retrieved_docs = retrieve_documents(test_subqueries)
    print(f"\nRetrieved {len(retrieved_docs)} unique documents.")
    
    for idx, doc in enumerate(retrieved_docs, 1):
        print(f"{idx}. {doc.text[:200]}... {doc.score}")  # Display snippet of each document"""
