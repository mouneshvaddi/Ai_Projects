
from langchain_ollama import ChatOllama

# Step 1: Connect to the local Ollama model
llm = ChatOllama(
    model="llama3.2",
    temperature=0.3
)

# Step 2: Send a question
response = llm.invoke(
        "Explain Generative AI in simple words with an example in 100 words."
)

# Step 3: Print the AI response
print("\nAI Response:")
print(response.content)
