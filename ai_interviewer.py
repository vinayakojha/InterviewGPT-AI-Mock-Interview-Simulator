from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-oss-20b"


# Generate Interview Questions
def generate_questions(resume_text, job_description):

    prompt = f"""
You are an expert technical interviewer.

Analyze the candidate resume and job description.

Generate exactly 20 interview questions.

Rules:
- One question per line
- Number each question
- Do NOT provide explanations
- Do NOT provide categories
- Do NOT provide tables

Example:

1. Tell me about yourself.

2. Why should we hire you?

3. Explain your AI Resume Analyzer project.

Questions should be personalized according to the candidate's resume.

Resume:
{resume_text}

Job Description:
{job_description}
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"


# Evaluate Candidate Answer
def evaluate_answer(question, answer):
    

    prompt = f"""
You are a professional interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer and provide:

1. Score out of 10
2. Strengths
3. Weaknesses
4. Areas of Improvement
5. Improved Sample Answer

Return the result in markdown format.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"