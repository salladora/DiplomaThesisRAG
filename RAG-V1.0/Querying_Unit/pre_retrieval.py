"""Preprocesses User Query for optimized Retrieval."""

#from llama_index.core.indices.query.query_transform import HyDEQueryTransform, DecomposeQueryTransform
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from openai import OpenAI as OpenAIClient
from config import OPENAI_API_KEY

client = OpenAIClient(api_key=OPENAI_API_KEY) 
llm = LlamaOpenAI(model="gpt-4o")

def rewrite_query(query: str)-> str:
    """
    Rewrites the user query to be clearer and more specific.

    Args:
        query: Original user Query

    Returns:
        Rewritten query as string
    """
    prompt_template = (
        "Rewrite the following query to be clearer and more specific. Keep abbreviations as they are and dont interpret their meaning:\n\n"
        f"Original Query: {query}\n\n"
        "Rewritten Query:"
        )
    prompt_text = prompt_template.format(query=query)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt_text}]
        )
   
    rewritten_query = response.choices[0].message.content 
    return rewritten_query

def decompose_query(query: str)-> list:
    """
    Splits the query into multiple simpler subqueries.

    Args:
        query: Rewritten query as string

    Returns:
        subqueries: List of multiple subqueries
    """
    #Query splitting prompt for LLM
    custom_decomposition_prompt = (
        "Zerlegen Sie die folgende komplexe Frage in mehrere einfachere Fragen.\n"
        "Erfinden Sie keine neuen Aspekte zur ursprünglichen Frage, sondern nehmen Sie nur die Fragen auf, die Teil der ursprünglichen Eingabe waren.\n"
        "Schreiben Sie jede Frage in eine neue Zeile."
        "Jede Frage sollte sich auf einen einzelnen Aspekt der ursprünglichen Frage konzentrieren.\n\n"
        f"Original Query: {query}\n\n"
        "Decomposed Queries:"
    )
    #Passes Prompt and query to LLM
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": custom_decomposition_prompt}]
    )
    decomposed_queries = response.choices[0].message.content.strip().split("\n")
    print(decomposed_queries)

    return decomposed_queries

# Full Pre-Retrieval Pipeline
def preprocess_query(query: str) -> list:
    """
    Rewrites and decomposes a query for better retrieval.

    Args:
        query: User Query to be processed and imprpved
    Returns:
        subqueries: List of improved atomized subqueries for Pinecone retrieval
    """
    # Step 1: Rewrite
    rewritten_query = rewrite_query(query) 
    # Step 2: Decompose 
    subqueries = decompose_query(rewritten_query)  
    return subqueries

# Tests the functions
if __name__ == "__main__":
    test_query = "What are e-tutors and wat function do they serve in the context of VCL?"
    
    #processed_queries = preprocess_query(test_query)
    #print("list: ", type(processed_queries))
    #print(f"\nGenerated Subqueries: {processed_queries}")



# Query Expansion using HyDE
"""def expand_query(query: str): #-> str
    transformer = HyDEQueryTransform(llm=llm)
    expanded_query = transformer.run(query)
    print(f"expanded: {expanded_query}")
    return expanded_query"""


# Query Decomposition (Splitting a complex query into subqueries)
"""def decompose_query(query: str) -> list:
    transformer = DecomposeQueryTransform(llm=llm)
    query_bundle = transformer.run(query)
    print(f"\nDEBUG: QueryBundle Output → {query_bundle}")  
    #subqueries = [subquery for subquery in query_bundle.sub_queries]
    return query_bundle"""