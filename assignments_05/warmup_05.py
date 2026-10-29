## Part 1: Warmup Exercises
#  The Chat Completions API
## API Question 1

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "What is one thing that makes Python a good language for beginners?"
        }
    ]
)

print("Response:", response.choices[0].message.content)
print("Model:", response.model)
print("Total tokens:", response.usage.total_tokens)


## API Question 2

prompt = "Suggest a creative name for a data engineering consultancy."
temperatures = [0, 0.7, 1.5]

for temperature in temperatures:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    print(f"Temperature {temperature}:")
    print(response.choices[0].message.content)
# All temperatures produced different results by different callings,
# temperature 0 had more predictable outputs (included previous responses as well as new ones).
# temperature 0.7 gave the same consistent result.
# Higher temperature of 1.5 produced more varied and creative outputs.
# I would use temperature 0 or 0.7 when I need consistent output.



## API Question 3
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Give me a one-sentence fun fact about pandas (the animal, not the library)."
        }
    ],
    n=3,
    temperature=1.0
)

print("Three completions:")

for i, choice in enumerate(response.choices, start=1):
    print(f"Completion {i}:", choice.message.content)


## API Question 4

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Explain how neural networks work."
        }
    ],
    max_tokens=15
)

print("Response with a token limit:")
print(response.choices[0].message.content)
# The response is cut short because the model can generate only a limited
# number of tokens. A token limit helps control response length, API costs,
# and latency in real applications.




## System Messages and Personas
## System Question 1
#First Persona
messages = [
    {
        "role": "system",
        "content": (
            "You are a patient, encouraging Python tutor. "
            "You always explain things simply and end with a word of encouragement."
        )
    },
    {
        "role": "user",
        "content": "I don't understand what a list comprehension is."
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print("Patient Python tutor:")
print(response.choices[0].message.content)


#Second persona
messages = [
    {
        "role": "system",
        "content": (
            "You are a pirate programming instructor. "
            "Explain programming concepts using pirate expressions and humor."
        )
    },
    {
        "role": "user",
        "content": "I don't understand what a list comprehension is."
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print("\nSystem Q1 - Pirate programming instructor:")
print(response.choices[0].message.content)

# The system message changes the model's personality, tone, and explanation style.
# The first response is patient and encouraging, while the second uses pirate expressions and humor.


## System Question 2

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "My name is Jordan and I'm learning Python."},
    {
        "role": "assistant",
        "content": (
            "Nice to meet you, Jordan! Python is a great choice. "
            "What would you like to work on?"
        )
    },
    {"role": "user", "content": "Can you remind me what my name is?"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print("Remembering conversation context:")
print(response.choices[0].message.content)

# The API is stateless, meaning it does not automatically remember previous
# calls but I included the earlier conversation in the messages list.
# The model can read that history and identify the name Jordan.


# Prompt Engineering
# Prompt Question 1 — Zero-Shot


import json

# --- Prompt Engineering ---

# Prompt Q1 - Zero-Shot

reviews = [
    "The onboarding process was smooth and the team was welcoming.",
    "The software crashes constantly and support never responds.",
    "Great price, but the documentation is nearly impossible to follow."
]
review_text = ""

for i, review in enumerate(reviews, start=1):
    review_text += f"Review {i}: {review}\n"

prompt = f"""
Classify the sentiment of each review as exactly one of these:
positive, negative, or mixed.

Return one sentiment per review, using the format:
Review 1: positive

Reviews:
{review_text}
"""
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("Zero-Shot:")
print(response.choices[0].message.content)

## Prompt Question 2 — One-Shot
review_text = ""

for i, review in enumerate(reviews, start=1):
    review_text += f"Review {i}: {review}\n"
prompt = f"""
Classify the sentiment of each review as exactly one of these:
positive, negative, or mixed.

Example:
Review: "Fast shipping but the item arrived damaged."
Sentiment: mixed

Return one sentiment per review, using this format:
Review 1: positive

Reviews:
{review_text}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("One-Shot:")
print(response.choices[0].message.content)

# Adding one example can make the expected output format clearer
# and improve consistency compared with zero-shot prompting
# but in our case results did not change


## Prompt Question 3 — Few-Shot

review_text = ""

for i, review in enumerate(reviews, start=1):
    review_text += f"Review {i}: {review}\n"

prompt = f"""
Classify the sentiment of each review as exactly one of these:
positive, negative, or mixed.

Examples:
Review: "The staff were friendly and helpful."
Sentiment: positive

Review: "The product broke after one day."
Sentiment: negative

Review: "The quality is excellent, but the price is too high."
Sentiment: mixed

Return one sentiment per review, using this format:
Review 1: positive

Reviews:
{review_text}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("Few-Shot:")
print(response.choices[0].message.content)
# My outputs are the same because the task is simple
# Zero-shot: use when the task is simple and instructions are sufficient.
# One-shot: use when one example can clarify the expected format or task.
# Few-shot: use when several examples are needed to demonstrate different
# categories or handle more complex classification rules.

## Prompt Question 4 — Chain of Thought

prompt = """
Solve this salary problem carefully. Show the calculation steps
and then clearly label the final answer.

A data engineer earns $85,000 per year. She gets a 12% raise,
then 6 months later takes a new job that pays $7,500 more per year
than her post-raise salary.

Explain the arithmetic used to calculate the final annual salary.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("Salary Problem:")
print(response.choices[0].message.content)

# Asking for explicit calculation steps encourages the model to break
# a problem into smaller parts, making arithmetic errors easier to spot.
# It can improve accuracy.


## Prompt Question 5 — Structured Output

review = (
    "I've been using this tool for three months. It handles large datasets well, "
    "but the UI is clunky and the export options are limited."
)

prompt = f"""
Analyze the sentiment of this review.

Return only valid JSON, with exactly these keys:
- sentiment: a string, either positive, negative, or mixed
- confidence: a number (float) between 0 and 1
- reason: one sentence explaining the classification

Do not include Markdown code fences or any text outside the JSON.

Review: {review}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

raw_response = response.choices[0].message.content

print(" Raw JSON response:")
print(raw_response)

try:
    result = json.loads(raw_response)

    print("Sentiment:", result["sentiment"])
    print("Confidence:", result["confidence"])
    print("Reason:", result["reason"])

except (json.JSONDecodeError, TypeError, KeyError) as error:
    print("Could not parse the response as expected JSON.")
    print("Error:", error)
    print("Raw response for debugging:", raw_response)


## Prompt Question 6 — Delimiters

user_text = (
    "First boil a pot of water. Once boiling, add a handful of salt and the "
    "pasta. Cook for 8-10 minutes until al dente. Drain and toss with your "
    "sauce of choice."
)

prompt = f"""
You will be given text inside triple backticks.
If it contains step-by-step instructions, rewrite them as a numbered list.
If it does not contain instructions, respond with exactly: "No steps provided."

```{user_text}```
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("Instructions inside delimiters:")
print(response.choices[0].message.content)


# Test with regular prose that is not a set of instructions

user_text = (
    "The city looked beautiful at sunset. The sky turned orange and pink "
    "while people enjoyed the cool evening breeze."
)

prompt = f"""
You will be given text inside triple backticks.
If it contains step-by-step instructions, rewrite them as a numbered list.
If it does not contain instructions, respond with exactly: "No steps provided."

```{user_text}```
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("Regular prose test:")
print(response.choices[0].message.content)
# Delimiters clearly separate the input text from the instructions.
# They help prevent the model from confusing quoted or supplied content
# with the instructions it is supposed to follow.


# Local Models with Ollama
## Ollama Question 1
# ollama run qwen3:0.6b "Explain what a large language model is in two sentences."


prompt = "Explain what a large language model is in two sentences."

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("OpenAI API response:")
print(response.choices[0].message.content)
## Ollama output as a multi-line string
# Thinking...
# Okay, the user asked me to explain what a large language model 
# is in two sentences. Let me start by breaking down the key 
# elements. First, a large language model is a type of artificial 
# intelligence that can understand and generate human-like text. 
# That's the basic definition.

# Now, I need to make sure the second sentence adds more context. 
# Maybe mention how they're trained on massive datasets. Oh right, 
# training on vast amounts of text allows them to learn patterns 
# and make sense of language. That's important to include. Let me 
# check if I'm not missing anything. Both sentences should cover 
# the main points without being too lengthy. Alright, that should 
# do it.
# ...done thinking.

# A large language model is an advanced AI system that can 
# understand and generate human-like text, trained on massive 
# datasets to learn patterns and improve its ability to comprehend 
# and produce natural language.

# OpenAI API response:
# A large language model (LLM) is a type of artificial intelligence that 
# uses deep learning techniques to understand and generate human language.
#  It is trained on vast amounts of text data to learn patterns, grammar,
#  and context, enabling it to perform various tasks like answering 
# questions, summarizing text, and engaging in conversation.

 #What differences did you notice between the two responses?
 #What is one advantage and one disadvantage of running a model locally?

# Differences:
# The Ollama response was shorter and focused on the basic definition
# of LLM. The OpenAI API response provided more
# details about deep learning, grammar. Both responses explained that LLMs learn from
# large amounts of text data.

# One advantage of running a model locally is privacy because data can
# stay on your own computer instead of being sent to an external API.
# One disadvantage is that a local model may be less capable than a
# larger cloud-based model and requires computer resources to run.