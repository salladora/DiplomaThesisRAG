"""Pre-processes chunks retrieved from Pinecone for better response generation."""

from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from openai import OpenAI as OpenAIClient
import openai
from retrieval import retrieve_documents
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
client = OpenAIClient(api_key=OPENAI_API_KEY) 
llm = LlamaOpenAI(model="gpt-4o")

def rerank_results(documents: list, query: str) -> list:
    """
    Reranks chunks using cross-encoder/ms-marco-MiniLM-L-2-v2

    Args:
        documents : List of retrieved Chunks
        query : Rewritten but not split user query

    Returns: 
        rerank_results: List of retrieved chunks with improved prioritization 
    """
    reranker = SentenceTransformerRerank(top_n=8, model="cross-encoder/ms-marco-MiniLM-L-2-v2")
    rerank_results = reranker.postprocess_nodes(documents, query_str= query)
    return rerank_results


def summarize_results(documents:list, query: str) -> str:
    """Summarizes retrieved chunks to handle redundancy.

    Args:
        documents: List of retrieved and reranked chunks
        query: Rewritten but not split user query
    Returns:
        summarized_response: Summary of all chunks as String
    """
    custom_summarization_prompt = (
        f"Gegeben ist diese Query: {query}\n\n"
        "Überprüfe die folgenden Texabschnitte und entferne inhalte, die zur Beantwortung der query nicht relevant sind. \n"
        "Überprüfe auch, ob sich Inhalte doppeln oder redundant sind und bereinige die Dopplung.\n\n"
        f"Textabschnitte: {documents} \n\n"
        "Bereiningte Inhalte: "
    )
    #Passes Prompt and query to LLM
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": custom_summarization_prompt}]
    )
    
    summarized_response = response.choices[0].message.content.strip()
    print(summarized_response)
    return summarized_response





# Full Post-Retrieval Processing
def process_retrieved_docs(documents, query)-> str:
    """ Full post-retriveal processing.

    Reranks and summarizes retrieved chunks absed on improved user query.
    
    Args:
        documents: List of retrieved chunks
        query: Rewritten but not split user query
    Returns:
        summarized_response: Summary of all chunks as String
    """
    reranked_docs = rerank_results(documents, query)
    summarized_response = summarize_results(reranked_docs, query)
    return summarized_response

# Test the post-retrieval pipeline
if __name__ == "__main__":
    test_query = "what are design dimensions of virtual collaborative learning?"
    test_subquery = [test_query]
    retrieved_docs = retrieve_documents(test_subquery)
    final_response = process_retrieved_docs(retrieved_docs, test_query)

"""if __name__ == "__main__":
    test_query = "How does quantum computing impact AI?"
    test_docs = [
        {"text": "Quantum computing enables faster optimizations in AI...", "score": 0.8},
        {"text": "AI models can leverage quantum computing for efficiency...", "score": 0.7},
        {"text": "Quantum AI has the potential to revolutionize deep learning...", "score": 0.9},
    ]
    
    final_response = process_retrieved_docs(test_docs, test_query)
    print("\nFinal Summarized Response:\n", final_response)"""
    