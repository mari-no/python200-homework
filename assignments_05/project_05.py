## Task 1: Setup and System Prompt


from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def get_completion(messages, model="gpt-4o-mini", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=400
    )
    return response.choices[0].message.content

SYSTEM_PROMPT = """
You are a professional Job Application Coach who helps job seekers
prepare clear, accurate, and tailored application materials for
specific job opportunities.

Your primary audience is job seekers applying for roles in technology,
including software engineering, QA engineering, software testing,
and project management. Help users communicate their skills,
professional experience, achievements, and transferable skills
effectively to recruiters and hiring managers.

Your responsibilities include:
- Helping users improve resumes, cover letters, and professional summaries.
- Tailoring application materials to a specific job description.
- Improving grammar, clarity, tone, and professional English.
- Helping users prepare answers to job application questions.
- Suggesting ways to describe achievements using specific examples
  and measurable results when the user provides supporting facts.
- Identifying missing information and asking clarifying questions
  when necessary.

Behavioral constraints:
1. Stay focused on job applications, career-related writing,
   and preparation directly connected to applying for jobs.
2. Never invent qualifications, work experience, certifications,
   technical skills, employers, or achievements. Never change
   the scale, timing, or outcome of an achievement. If information
   is missing, ask the user or clearly mark it as a suggestion.
3. Preserve the user's intended meaning and professional background.
   Make improvements without misrepresenting their experience.
4. Use clear, natural, professional language that is appropriate
   for recruiters and hiring managers.
5. Always remind the user to review and edit your output before
   submitting it to an employer or publishing it anywhere.
6. Acknowledge that you may not know the specific industry norms,
   company culture, recruiter preferences, or expectations for every
   role. Encourage the user to apply their own judgment and verify
   that the recommendations fit their target industry and position.
7. When possible, explain important edits briefly so users can
   understand and learn from the suggestions.
8. If a request is unrelated to job applications or career preparation,
   politely redirect the conversation to the assistant's intended purpose.

Your goal is to help users present their real qualifications confidently,
professionally, and honestly while keeping them in control of their
final application materials.
"""


messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": "Help me write a professional summary for a QA Engineer resume."
    }
]

answer = get_completion(messages)
print(answer)


# I explicitly instruct the coach not to invent qualifications or
# achievements because inaccurate claims could harm a job seeker's
# credibility during the hiring process.

## Task 2: Bullet Point Rewriter

import json


def rewrite_bullets(bullets: list[str]) -> list[dict]:
    # Separate the user's resume bullets from the instructions using delimiters.
    bullet_text = "\n".join(f"- {b}" for b in bullets)

    prompt = f"""
    You are a professional resume coach helping a career changer
    improve their resume.

    Rewrite each resume bullet point to make it more specific,
    results-oriented, concise, and compelling.

    Instructions:
    - Start with a strong action verb.
    - Emphasize responsibilities, skills, and outcomes.
    - Preserve the original meaning and facts.
    - Do not invent metrics, achievements, or responsibilities.
    - If the original lacks details, improve the wording without
      making unsupported claims.
    - Keep each improved bullet appropriate for a professional resume.

    Return a raw JSON array only. Do not wrap the response in Markdown
    code fences. Do not include ```json, ```, explanations, or any
    other text outside the JSON array. 
    Each item must have exactly two keys:
    "original" (the original bullet) and
    "improved" (the rewritten bullet).

    <resume_bullets>
    {bullet_text}
    </resume_bullets>
    """

    messages = [{"role": "user", "content": prompt}]

    # Call the helper function from Task 1.
    response = get_completion(messages)


# Convert the response from JSON text into a Python list.
    try:
        result = json.loads(response)
    except json.JSONDecodeError as e:
        print("The model did not return valid JSON.")
        raise ValueError(
                f"Could not parse model response: {response!r}"
            ) from e

    # Print the original and improved versions side by side.
    for item in result:
        print(f"Original:  {item['original']}")
        print(f"Improved:  {item['improved']}")
        print("-" * 60)
    

    return result


# Test the function with the starter bullets.
bullets = [
    "Helped customers with their problems",
    "Made reports for the management team",
    "Worked with a team to finish the project on time"
]

results = rewrite_bullets(bullets)

# Improvements feel meaningfully better, suggested stronger
# action verbs and clearer descriptions:
# Original:  Helped customers with their problems
# Improved:  Resolved customer issues by providing tailored solutions and support.
# ------------------------------------------------------------
# Original:  Made reports for the management team
# Improved:  Compiled and presented detailed reports to the management team to inform strategic decision-making.
# ------------------------------------------------------------
# Original:  Worked with a team to finish the project on time
# Improved:  Collaborated with a cross-functional team to successfully complete the project ahead of schedule.


## Task 3: Cover Letter Generator

def generate_cover_letter(job_title: str, background: str) -> str:
    prompt = f"""
    You write strong cover letter opening paragraphs for career changers.
    The paragraph should be 3-5 sentences: confident, specific, and free of clichés.

    Use the examples to learn the desired tone and structure.
    Do not copy their details into the new paragraph.
    Use only the qualifications and experience provided in the new background.
    Do not invent employers, achievements, credentials, or technical skills.
    Connect the person's previous experience to the target role with specific examples.

    Here are two examples of the style and tone you should match:

    Example 1:
    Role: Data Analyst at a healthcare nonprofit
    Background: Seven years as a registered nurse, recently completed a data analytics bootcamp.
    Opening: After seven years as a registered nurse, I've spent my career making decisions
    under pressure using incomplete information — which turns out to be excellent training for
    data analysis. I recently completed a data analytics program where I built dashboards
    tracking patient outcomes across departments. I'm excited to bring that combination of
    clinical context and technical skill to [Company]'s mission-driven work.

    Example 2:
    Role: Junior Software Engineer at a fintech startup
    Background: Ten years in retail banking operations, self-taught Python developer for two years.
    Opening: I spent a decade on the operations side of banking, watching technology decisions
    get made by people who had never processed a wire transfer or resolved a failed ACH batch.
    That frustration turned into curiosity, and two years of self-teaching Python later, I'm
    ready to be on the other side of those decisions. I'm applying to [Company] because your
    work on payment infrastructure is exactly where my domain expertise and new technical skills
    intersect.

    Now write an opening paragraph for this person:

    Role: {job_title}
    Background: {background}

    Opening:
    """

    messages = [{"role": "user", "content": prompt}]

    # Generate and return the cover letter opening
    return get_completion(messages)


# Test the function
job_title = "Junior Data Engineer"
background = (
    "Five years of experience as a middle school math teacher; "
    "recently completed a Python course and built data pipelines using Pandas."
)

cover_letter = generate_cover_letter(job_title, background)
print(cover_letter)

# I chose examples that connect previous careers to new technical roles
# through concrete experience. Few-shot prompting helps control the tone, 
# specificity, length, and structure of the model's response.


## Task 4: Moderation Check

def is_safe(text: str) -> bool:
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )

    flagged = result.results[0].flagged

    if flagged:
        print(
            "Your message couldn't be processed. "
            "Please rephrase it and try again."
        )
        return False

    return True
# Test with a safe input
print(is_safe("Help me improve my resume for a QA Engineer position."))

# Test with an input that should be flagged
print(is_safe("I want to kill someone and carry out a violent attack."))

# Test borderline
print(is_safe("I am so angry at my boss that I could hurt him."))



## Task 5: The Chatbot Loop

def run_chatbot():
    # 1. Initialize conversation history with your system prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("=" * 50)
    print("Job Application Helper")
    print("=" * 50)
    print("I can help you with:")
    print("  1. Rewriting resume bullet points")
    print("  2. Drafting a cover letter opening")
    print("  3. Any other questions about your application")
    print("\nType 'quit' at any time to exit.\n")

    while True:
        user_input = input("You: ").strip()

        # 2. Handle exit
        if user_input.lower() in {"quit", "exit"}:
            print("\nJob Application Helper: Good luck with your applications!")
            break

        # 3. Skip empty input
        if not user_input:
            continue

        # 4. Run moderation check before doing anything else
        if not is_safe(user_input):
            continue

        
        # 5. Check if the user wants to rewrite bullets
        #    (hint: look for keywords like "bullet" or "resume" in user_input.lower())
        if "bullet" in user_input.lower() or "resume" in user_input.lower():
            print("\nJob Application Helper: Paste your bullet points below, one per line.")
            print("When you're done, type 'DONE' on its own line.\n")

            raw_bullets = []
            while True:
                line = input().strip()
                if line.upper() == "DONE":
                    break
                if line:
                    raw_bullets.append(line)

            results = rewrite_bullets(raw_bullets)

            print("\nJob Application Helper: Here are your improved bullet points:")
            for item in results:
                print(f"\nOriginal: {item['original']}")
                print(f"Improved: {item['improved']}")

        # 6. Check if the user wants a cover letter
        elif "cover letter" in user_input.lower():
            job_title = input("Job Application Helper: What is the job title? ").strip()
            background = input("Job Application Helper: Briefly describe your background: ").strip()

            cover_letter = generate_cover_letter(job_title, background)

            print("\nJob Application Helper:")
            print(cover_letter)

        # 7. Otherwise, handle it as a regular chat turn
        else:
            messages.append({"role": "user", "content": user_input})

            reply = get_completion(messages)

            print("\nJob Application Helper:", reply)

            messages.append({"role": "assistant", "content": reply})
       
            pass


if __name__ == "__main__":
    run_chatbot()
# Task 6: Ethics Reflection
# AI-generated career advice can be biased because language models
# learn from existing text that may overrepresent certain industries,
# communication styles, and cultural backgrounds. As a result, the
# chatbot might favor particular ways of describing experience and
# overlook the strengths of people from different backgrounds.
#
# If a job seeker submits AI-generated content without reviewing it,
# the chatbot might include inaccurate information, exaggerate
# achievements, or describe skills and experience the person does
# not actually have. This could damage the applicant's credibility
# and create problems during an interview or background check.
#
# One important guardrail is to remind users to review and verify
# all generated content before submitting it to an employer.(Disclaimer)

