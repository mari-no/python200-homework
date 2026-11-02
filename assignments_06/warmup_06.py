from dotenv import load_dotenv
import os

if load_dotenv():
    print("API key loaded successfully.")
else:
    print("Warning: could not load API key. Check your .env file.")

#RAG Concepts
## Concepts Question 1

# RAG Concepts

# Scenario A: A legal team wants an assistant that can 
# answer questions about their internal policy library —
#  hundreds of PDFs that are updated every quarter.
# RAG allows the model to access the latest documents
# without retraining or fine-tuning the model every time
# the policies change.

# Scenario B: A startup wants their model to write product 
# copy in a very specific brand voice — a dry, minimalist 
# style that does not appear much online. They have 3,000 
# examples their in-house writers produced over the years.
# Fine-tuning is the best approach because the startup has 3,000 examples 
# of its desired brand voice. Training the model on these
# examples can help it consistently reproduce the specific 
# writing style, tone, and language patterns.


# Scenario C: A data analyst needs to ask an LLM questions 
# about a single two-page report she just received.
#  She does not need this to work for any other document.
# Prompt engineering is sufficient because the task involves only one short document
# and does not require a reusable knowledge base.

## Concepts Question 2
# AI hallucinations (responses that sound confident but are wrong) 
# can be particularly difficult to detect. 
# Why is a confidently wrong answer more harmful than one that says 
# "I am not sure"? 
# A confidently wrong answer is more harmful than an answer that admits
# uncertainty because users are more likely to trust information presented
# with confidence and may act on it without verifying whether it is correct.
# For example, in a medical situation, an AI assistant might confidently
# recommend an incorrect medication dosage. A patient could follow that
# recommendation and suffer serious health consequences.

## Concepts Question 3

steps = [
    "1. Extract text from source documents",
    # Read PDFs, Word documents, or other files and extract their text content.

    "2. Split text into chunks",
    # Divide the extracted text into smaller, manageable pieces so the model
    # can retrieve specific information rather than process entire documents.

    "3. Convert text chunks into embeddings",
    # Transform each text chunk into a numerical vector that represents
    # its semantic meaning.

    "4. Receive the user's query",
    # Accept the user's question that the system needs to answer.

    "5. Embed the user's query",
    # Convert the question into a numerical vector using the same embedding model
    # so it can be compared with the document chunks.

    "6. Retrieve the most relevant chunks",
    # Compare the query embedding with stored document embeddings and find
    # the chunks that are most semantically relevant to the question.

    "7. Inject retrieved chunks into the prompt",
    # Add the retrieved information to the LLM prompt as additional context.

    "8. Generate a response from the LLM",
    # The LLM uses the user's question and retrieved context to generate
    # a relevant, hopefully accurate, response.
]

## Keyword RAG

import string

def simple_keyword_retrieval(query, documents, verbose=True):
    """Keyword retrieval using token overlap scoring."""
    stopwords = {
        "a", "an", "the", "and", "or", "in", "on", "of", "for", "to", "is",
        "are", "was", "were", "by", "with", "at", "from", "that", "this",
        "as", "be", "it", "its", "their", "they", "we", "you", "our"
    }
    translator = str.maketrans("", "", string.punctuation)

    query_words = {
        w.translate(translator)
        for w in query.lower().split()
        if w not in stopwords
    }
    if verbose:
        print(f"\nQuery tokens (filtered): {sorted(query_words)}")

    scores = []
    for name, content in documents.items():
        content_words = {
            w.translate(translator)
            for w in content.lower().split()
            if w not in stopwords
        }
        overlap = query_words & content_words
        score = len(overlap)
        scores.append((score, name, content))
        if verbose:
            print(f"[{name}] overlap={score} -> {sorted(overlap)}")

    scores.sort(reverse=True)
    best = next(((name, content) for score, name, content in scores if score > 0), None)
    if best:
        if verbose:
            print(f"\nSelected best match: {best[0]}")
        return [best]
    else:
        if verbose:
            print("\nNo overlapping keywords found.")
        return [("None found", "No relevant content.")]
## Keyword Question 1

query = "What are your hours on weekends?"

documents = {
    "menu.txt": "We serve espresso, lattes, cappuccinos, and cold brew. Pastries include croissants and muffins baked fresh daily. Oat milk and almond milk are available.",
    "hours.txt": "We are open Monday through Friday from 7am to 7pm. On weekends we open at 8am and close at 5pm. We are closed on Thanksgiving and Christmas Day.",
    "hiring.txt": "We are currently hiring baristas and shift supervisors. Send your resume to jobs@groundworkcoffee.com.",
    "loyalty.txt": "Join our loyalty program to earn one point per dollar spent. Redeem 100 points for a free drink of your choice.",
}


results = simple_keyword_retrieval(query, documents, verbose=True)

print(results[0][0])
#loyaty.txt wins and it's not what was expected by me or user.
# When scores are equal, Python compares the document names 
# alphabetically in reverse order. That's why loyalty.txt wins.
# To avoid that, word "your" must be added to stopwords 
# set in simple_keyword_retrieval
# Query tokens (filtered): ['hours', 'weekends', 'what', 'your']
# [menu.txt] overlap=0 -> []
# [hours.txt] overlap=1 -> ['weekends']
# [hiring.txt] overlap=1 -> ['your']
# [loyalty.txt] overlap=1 -> ['your']

# Selected best match: loyalty.txt
# Selected document: loyalty.txt

## Keyword Question 2
query = "Do you have anything without caffeine?"

documents = {
    "menu.txt": "We serve espresso, lattes, cappuccinos, and cold brew. Pastries include croissants and muffins baked fresh daily. Oat milk and almond milk are available.",
    "hours.txt": "We are open Monday through Friday from 7am to 7pm. On weekends we open at 8am and close at 5pm. We are closed on Thanksgiving and Christmas Day.",
    "hiring.txt": "We are currently hiring baristas and shift supervisors. Send your resume to jobs@groundworkcoffee.com.",
    "loyalty.txt": "Join our loyalty program to earn one point per dollar spent. Redeem 100 points for a free drink of your choice.",
}

results = simple_keyword_retrieval(query, documents, verbose=True)

print("Selected document for question 2:", results[0][0])
# No documents were selected because no overlap was found
# Keyword RAG fails in this case because it relies on exact keyword
# matching and cannot understand synonyms or semantic relationships.
# Although the menu contains information about different drinks, it
# does not explicitly mention caffeine.
# Semantic retrieval using embeddings would perform better because
# it can identify related concepts even when the exact words differ.
# Query tokens (filtered): ['anything', 'caffeine', 'do', 'have', 'without']
# [menu.txt] overlap=0 -> []
# [hours.txt] overlap=0 -> []
# [hiring.txt] overlap=0 -> []
# [loyalty.txt] overlap=0 -> []
# No overlapping keywords found.
# Selected document for question 2: None found

## Keyword Question 3
query = "How do I sign up for rewards?"
# I predict it will return None because there's no overlap
documents = {
    "menu.txt": "We serve espresso, lattes, cappuccinos, and cold brew. Pastries include croissants and muffins baked fresh daily. Oat milk and almond milk are available.",
    "hours.txt": "We are open Monday through Friday from 7am to 7pm. On weekends we open at 8am and close at 5pm. We are closed on Thanksgiving and Christmas Day.",
    "hiring.txt": "We are currently hiring baristas and shift supervisors. Send your resume to jobs@groundworkcoffee.com.",
    "loyalty.txt": "Join our loyalty program to earn one point per dollar spent. Redeem 100 points for a free drink of your choice.",
}

results = simple_keyword_retrieval(query, documents, verbose=True)

print("Selected document for question 3:", results[0][0])
# My prediction was correct:

# No overlapping keywords found.
# Selected document for question 2: None found

# Query tokens (filtered): ['do', 'how', 'i', 'rewards', 'sign', 'up']
# [menu.txt] overlap=0 -> []
# [hours.txt] overlap=0 -> []
# [hiring.txt] overlap=0 -> []
# [loyalty.txt] overlap=0 -> []

# No overlapping keywords found.
# Selected document for question 3: None found


# Semantic RAG Concepts
## Semantic Question 1
# 1. What is a vector embedding?
# A vector embedding is a numerical representation of text that captures
# its meaning and context. It converts words or sentences into numbers
# so that a computer can compare how similar their meanings are.
# 2. Two text chunks have cosine similarity scores of 0.85 and 0.30 with 
# a given query. Which chunk is more relevant, and what does that number 
# tell you about the relationship between the texts?
# A higher score means the text is more similar in meaning to the query.
# A score of 0.30 indicates significantly weaker semantic relationship.
# 3. Why can semantic search find a relevant chunk even when none of 
# the exact words from the query appear in the chunk?
# Semantic search compares the meanings of texts, not just looking
# for identical words. For example, a query asking about "rewards"
# might match a chunk discussing a "loyalty program" because their
# meanings are related, even though they use different words.

# Semantic Question 2
# Keyword RAG and semantic RAG handle the same problem differently. 

# | Feature                    | Keyword RAG                       | Semantic RAG                                  |
# |----------------------------|-----------------------------------|-----------------------------------------------|
# | What is compared?          | Exact word overlap                | Meaning represented by vector embeddings      |
# | What is retrieved?         | Full document                     | Most relevant text chunks                     |
# | Can it handle synonyms?    | No                                | Yes       |
# | Storage format             | Plain text dictionary             | Vector embeddings stored in a vector database |
# | Relevance score            | Number of overlapping keywords    | Cosine similarity score                       |


# ## LlamaIndex
# For this section you will build a small LlamaIndex pipeline using the Brightleaf Solar PDFs 
#from the lesson. These documents should already be familiar from the lesson material.
from pathlib import Path

pdf_path = Path("lessons/06_AI_augmentation/resources/brightleaf_pdfs")

print("Directory exists:", pdf_path.exists())

from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4o-mini")
## LlamaIndex Question 1

# Load Brightleaf Solar PDF documents
documents = SimpleDirectoryReader(
    str(pdf_path)
).load_data()

print(f"Loaded {len(documents)} document pages.")


# Build an in-memory vector index
index = VectorStoreIndex.from_documents(documents)

print("Vector index created successfully!")


# Create a query engine that retrieves the 3 most relevant chunks
query_engine = index.as_query_engine(similarity_top_k=3)


# Questions to test
questions = [
    "What employee benefits does BrightLeaf offer?",
    "What are BrightLeaf's security policies?",
]


# Run each question and inspect the retrieved chunks
for question in questions:

    print(f"Question: {question}")
  

    response = query_engine.query(question)

    print("\nAnswer:")
    print(response)

    print("\nRetrieved source nodes:")

    for i, source_node in enumerate(response.source_nodes, start=1):

        print(f"\nSource node {i}")
        print(f"Similarity score: {source_node.score:.4f}")

        chunk_text = source_node.node.get_content()
        print(f"Chunk preview: {chunk_text[:150]}")
# Question 1: What employee benefits does BrightLeaf offer?
# The first retrieved chunk was highly relevant, with a similarity score
# of 0.7589. The other two chunks were about a partnership and
# the company's general overview, so they were not directly relevant,
# even though similarity scores for them were 0.5878 and 0.5609 accordingly.
# The model provided a confident and detailed answer.

# Question 2: What are BrightLeaf's security policies?
# The first retrieved chunk was directly relevant to network and data
# security, with a similarity score of 0.6639. The other two chunks
# covered employee benefits and the company overview, which were not
# directly relevant. The model provided a confident and specific answer.

# The problem is that unrelated chunks still received relatively high scores 
# (0.56–0.61). A higher similarity score does not guarantee that a chunk 
# is relevant.
# Semantic retrieval identifies text that is mathematically similar to the 
# query in embedding space. It doesn't understand relevance perfectly.

## LlamaIndex Question 2
question = "What employee benefits does BrightLeaf offer?"

#Retrieve only the top 1 chunk
query_engine_1 = index.as_query_engine(similarity_top_k=1)
response_1 = query_engine_1.query(question)

print("SIMILARITY_TOP_K = 1")

print("\nAnswer:")
print(response_1)

print("\nRetrieved source nodes:")
for i, source_node in enumerate(response_1.source_nodes, start=1):
    print(f"Source node {i}: Similarity score = {source_node.score:.4f}")


#Retrieve the top 5 chunks
query_engine_5 = index.as_query_engine(similarity_top_k=5)
response_5 = query_engine_5.query(question)

print("SIMILARITY_TOP_K = 5")

print("\nAnswer:")
print(response_5)

print("\nRetrieved source nodes:")
for i, source_node in enumerate(response_5.source_nodes, start=1):
    print(f"Source node {i}: Similarity score = {source_node.score:.4f}")
# With similarity_top_k=1, the model generated a detailed answer based
# on the most relevant employee benefits chunk (similarity score: 0.7589).
# With similarity_top_k=5, the answer included additional details, such
# as telemedicine, hospitalization, and mindfulness sessions. 
# More context isn't always better. Additional
# chunks may contain irrelevant information, which can introduce
# noise, distract the LLM, or potentially lead to unsupported answers.
#
# The highest similarity score remained unchanged, while four additional
# chunks with lower similarity scores were retrieved.

## LlamaIndex Question 3
question = (
    "How does BrightLeaf support employees while ensuring "
    "the company's data and business operations remain secure?"
)

query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query(question)
print("LLAMAINDEX QUESTION 3")

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(response)

print("\nRetrieved source nodes:")

for i, source_node in enumerate(response.source_nodes, start=1):
    print(f"\nSource node {i}")
    print(f"Similarity score: {source_node.score:.4f}")
    print("Full chunk:")
    print(source_node.node.get_content())

# I expected this query to be challenging because it combines two topics:
# employee benefits and company security policies, which are described
# in separate documents.
#
# The actual result was successful. The retriever returned the Network
# and Data Security chunk as the first result (similarity: 0.6772)
# and the Employee Benefits chunk as the second result (similarity: 0.6588).
# The LLM successfully combined information from both documents to
# generate a relevant and detailed answer.

## LlamaIndex Question 4

from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
)

faithfulness_evaluator = FaithfulnessEvaluator(
    llm=OpenAI(model="gpt-4o-mini")
)

relevancy_evaluator = RelevancyEvaluator(
    llm=OpenAI(model="gpt-4o-mini")
)

query_engine_q1 = index.as_query_engine(similarity_top_k=3)

q = "What employee benefits does BrightLeaf offer?"

# Generate the response
response = query_engine_q1.query(q)

# Evaluate faithfulness
faithfulness_result = faithfulness_evaluator.evaluate_response(
    query=q,
    response=response
)

# Evaluate relevancy
relevancy_result = relevancy_evaluator.evaluate_response(
    query=q,
    response=response
)

print(" LlamaIndex Question 3: EMPLOYEE BENEFITS")

print("\nAnswer:")
print(response)

print("\nEvaluation scores:")
print(f"Faithfulness score: {faithfulness_result.score}")
print(f"Faithfulness feedback: {faithfulness_result.feedback}")

print(f"Relevancy score: {relevancy_result.score}")
print(f"Relevancy feedback: {relevancy_result.feedback}")

# Question about information not explicitly covered in the documents

q_missing = "What is BrightLeaf's policy on paid vacation days and sick leave?"

# Generate the response
response_missing = query_engine_q1.query(q_missing)

# Evaluate faithfulness
faithfulness_missing = faithfulness_evaluator.evaluate_response(
    query=q_missing,
    response=response_missing
)

# Evaluate relevancy
relevancy_missing = relevancy_evaluator.evaluate_response(
    query=q_missing,
    response=response_missing
)

print("LlamaIndex Question 3: MISSING INFORMATION")


print("\nAnswer:")
print(response_missing)

print("\nEvaluation scores:")
print(f"Faithfulness score: {faithfulness_missing.score}")
print(f"Faithfulness feedback: {faithfulness_missing.feedback}")

print(f"Relevancy score: {relevancy_missing.score}")
print(f"Relevancy feedback: {relevancy_missing.feedback}")


# What does a faithfulness score of 1.0 mean? What would a score of 0.0 indicate?
# A score of 1.0 means the generated answer is fully supported by the retrieved 
# context. A score of 0.0 indicates that the answer is not supported by the retrieved context.
# What does a relevancy score measure, and how is it different from faithfulness?
# Relevancy measures whether the generated answer addresses the user's question and
# is relevant to the retrieved context. Unlike faithfulness, which focuses on factual 
# support, relevancy focuses on how well the answer addresses the question.
# Did the scores change between your two queries? If so, why do you think that happened?
# The employee benefits question received a faithfulness score of 1.0 and a relevancy
# score of 1.0. The answer was supported by the retrieved documents and directly 
# addressed the question. The vacation and sick leave question received scores of 0.0 
# for both metrics. Although the model correctly stated that this information
# was not available in the documents, the evaluators marked the response
# as not faithful and not relevant.
# What is the "LLM-as-a-judge" approach, and why is it used for RAG evaluation 
# instead of a simple accuracy metric?
# LLM-as-a-judge uses a language model to evaluate another model's
# responses. It is useful for RAG evaluation because answers can be incorrect,
# but still measure as correct, making exact-match
# accuracy metrics insufficient.
