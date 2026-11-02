## Part 2: Mini-Project: Groundwork Coffee Co. Q&A Assistant

## Step 1: Setup
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

import os

if load_dotenv():
    print("API key loaded successfully.")
else:
    print("Warning: could not load API key. Check your .env file.")
from pathlib import Path

docs_dir = Path("lessons/06_AI_augmentation/resources/groundwork_docs")

assert docs_dir.exists(), f"Document directory not found: {docs_dir}"

## Step 2: Load the Documents

reader = SimpleDirectoryReader(
    input_dir=str(docs_dir),
    required_exts=[".txt"]
)

documents = reader.load_data()

print(f"\nLoaded {len(documents)} documents:")

for document in documents:
    print(document.metadata.get("file_name"))

##  Step 3: Build the Index and Query Engine
# Set the embedding model
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small"
)
Settings.llm = OpenAI(model="gpt-4o-mini")

# Build the vector index from loaded documents
index = VectorStoreIndex.from_documents(documents)

# Create the query engine
query_engine = index.as_query_engine(
    similarity_top_k=3
)

print("\nIndex built successfully. Ready to answer questions.")

## Step 4: Query the Assistant
questions = [
    "What are Groundwork's hours on weekends?",
    "Do you offer any dairy-free milk options?",
    "How does the loyalty program work?",
    "How did Groundwork Coffee get started?",
    "Do you offer catering or wholesale orders?",
]

for question in questions:
    response = query_engine.query(question)
    print(f"QUESTION: {question}")
    print(f"ANSWER: {response}")

    # Inspect the top retrieved source node
    if response.source_nodes:
        source_node = response.source_nodes[0]

        document_name = source_node.node.metadata.get(
            "file_name", "Unknown source"
        )
        similarity_score = source_node.score
        chunk_text = source_node.node.get_content()

        print("\nTOP RETRIEVED SOURCE:")
        print(f"Document: {document_name}")
        print(f"Similarity score: {similarity_score:.4f}")
        print(f"Chunk preview: {chunk_text[:200]}")
    else:
        print("\nNo source nodes were retrieved.")
# Answers were correct, confident and true
# Similarity score doesn't mean answer accuracy and vice versa,
# for example this question was answeres correct, even though similarity
# score is only 0.2951
# QUESTION: How does the loyalty program work?
# ANSWER: The loyalty program is free to join and allows you to earn one 
# point for every dollar spent. Once you accumulate 100 points, you can redeem 
# them for any free drink on the menu. You can sign up for the program at the
#  register or on the website.
# TOP RETRIEVED SOURCE:
# Document: faq.txt
# Similarity score: 0.2951

## Step 5: Find a Failure
question = (
    "Does Groundwork offer coconut milk, "
    "and how much extra does it cost?"
)

response = query_engine.query(question)
print("STEP 5: FIND A FAILURE")

print(f"\nQUESTION: {question}")
print(f"\nFULL RESPONSE:\n{response}")

print("\nALL RETRIEVED SOURCE NODES:")

for i, source_node in enumerate(response.source_nodes, start=1):
    document_name = source_node.node.metadata.get(
        "file_name", "Unknown source"
    )

    similarity_score = source_node.score
    chunk_text = source_node.node.get_content()

    print(f"\n--- Source #{i} ---")
    print(f"Document: {document_name}")
    print(f"Similarity score: {similarity_score:.4f}")
    print(f"Chunk preview: {chunk_text[:200]}")
# I asked:"Does Groundwork offer coconut milk, and 
# how much extra does it cost?" and expected it to be hard
# because there's no information on cocounut milk options
# First it stated that info is not listed, but in the end
# the model guessed that there is no extra cost anyway.
# When the retrieval failed, the model's tone did not change,
# it still sound confident.
# To improve the system, I would update the prompt to explicitly
# instruct the model not to make assumptions or invent missing
# information.

# Step 6: Reflection
# 1. LlamaIndex implementation:
# The main LlamaIndex RAG pipeline took approximately 7 lines of
# executable code to configure the embedding model, create the
# vector index, and build the query engine. Without LlamaIndex,
# I would need to implement or configure document chunking,
# embedding generation, vector storage, and similarity-based
# retrieval separately. This would require significantly more
# code and a deeper understanding of the underlying processes.
# 2. Another business use case:
# An HR department could use RAG to help employees find answers
# in internal company documents, such as health insurance
# policies, vacation rules, parental leave, and remote-work
# guidelines. Employees could ask questions in natural language
# and receive answers based on the company's actual documentation.
# 3. RAG limitations:
# RAG cannot fully prevent a language model from making
# unsupported assumptions or generating incorrect information,
# even when the correct documents are retrieved.