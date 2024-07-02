import requests

API_KEY = "f790e8dfc337066ee29d92fca6ac9637238fb99deaac55946e59843c569277e4"
LLM_URL = "https://api.together.ai/playground/chat/meta-llama/Llama-3-70b-chat-hf"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query_llm(prompt):
    response = requests.post(
        LLM_URL,
        headers=headers,
        json={"prompt": prompt, "max_tokens": 500}
    )
    response_data = response.json()
    return response_data.get("choices", [{}])[0].get("text", "")

def encode_query(query):
    prompt = f"Encode this query into a fixed-length vector representation: {query}"
    return query_llm(prompt)

def generate_answer(query, context):
    prompt = f"Generate a detailed response based on the following query and context: \n\nQuery: {query}\n\nContext: {context}"
    return query_llm(prompt)

# Create the RAG pipeline
def create_rag_pipeline():
    return {
        "retriever": encode_query,
        "generator": generate_answer
    }