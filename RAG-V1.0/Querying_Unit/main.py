from pre_retrieval import preprocess_query
from retrieval import retrieve_documents
from post_retrieval import process_retrieved_docs
from config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

def main()-> None:
    
    try: 
        # Step 1: Gets user query
        user_query = input("\nGib deine Anfrage ein: ")
    except Exception as e:
        print(f"Error while getting user query: {e}")
        return
    
    try:
        # Step 2: Pre-Retrieval Enhancements (Rewrite, Decompose)
        subqueries = preprocess_query(user_query)
        print(f"\nGenerated Subqueries: {subqueries}")
    except Exception as e:
        print(f"Error while preprocessing query: {e}")
        return
    
    try:
        # Step 3: Retrieves documents from Pinecone
        retrieved_docs = retrieve_documents(subqueries)
        print(f"\nRetrieved {len(retrieved_docs)} unique documents.")
    except Exception as e:
        print(f"Error while retrieving documents: {e}")
        return

    try:
        # Step 4: Post-Retrieval Processing (Rerank & Summarize)
        summarized_docs = process_retrieved_docs(retrieved_docs, user_query)
    except Exception as e:
        print(f"Error while processing retrieved documents: {e}")
        return
    
    try:
        # Step 5: Generates final response using GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du bist ein intelligenter KI Assistent einer Wissenschaftlerin. Du sprichst deutsch. "},
                {"role": "user", "content": summarized_docs}
            ]
        )
    except Exception as e:
        print(f"Error while generating AI response: {e}")
        return

    print("\n🔹 AI Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
