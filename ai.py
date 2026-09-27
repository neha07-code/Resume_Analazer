import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is missing. Please add it to your .env file."
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


def analyze_resume(resume_text, user_goal):

    prompt = f"""
You are a senior software engineer and hiring manager.

Evaluate the resume based on the user's goal.

User's goal:
"{user_goal}"

STRICT Rules:
- Extract only relevant skills for this goal.
- Remove irrelevant tools or skills.
- Identify real skill gaps.
- Generate roadmap only for missing skills.
- Make the output different based on the user's goal.
- Keep the roadmap practical.
- Generate interview questions related to the user's goal.
- Return ONLY valid JSON.
- Do not add markdown or explanation outside JSON.

Return JSON in exactly this format:

{{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": []
}}

Resume:
{resume_text}
"""

    try:

        response = client.chat.completions.create(
            model="openrouter/free",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict hiring manager."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("AI did not return valid JSON.")

        json_content = content[start:end]

        result = json.loads(json_content)

        return result

    except Exception as e:

        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }