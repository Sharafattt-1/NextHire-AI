import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_resume(resume_text):
    """
    Analyze the resume using Gemini AI and return JSON.
    """

    prompt = f"""
You are an expert ATS Resume Analyzer, Senior HR Recruiter, Career Coach, and Technical Interviewer.

Analyze the resume below and return ONLY valid JSON.

Rules:
- Do NOT use markdown.
- Do NOT wrap the JSON inside ```json.
- Do NOT explain anything.
- Return ONLY valid JSON.

Return JSON in exactly this format:

{{
    "ats_score": 85,
    "overall_rating": "Excellent",
    "experience_level": "Fresher",
    "resume_title": "Python Backend Developer",
    "resume_summary": "A professional summary of the candidate.",

    "strengths": [
        "Python",
        "Django",
        "REST APIs"
    ],

    "weaknesses": [
        "Weak professional summary",
        "No quantified achievements"
    ],

    "missing_skills": [
        "Docker",
        "AWS",
        "CI/CD"
    ],

    "recommended_roles": [
        "Python Developer",
        "Backend Developer",
        "Django Developer"
    ],

    "interview_questions": [
        "Explain Django ORM.",
        "Difference between GET and POST.",
        "What is REST API?",
        "Explain Docker."
    ],

    "learning_roadmap": [
        "Master Git & GitHub",
        "Learn Docker",
        "Learn PostgreSQL",
        "Learn AWS",
        "Deploy Django Applications"
    ],

    "suggestions": [
        "Improve your professional summary.",
        "Add measurable achievements.",
        "Include GitHub project links.",
        "Mention cloud technologies."
    ]
}}

Resume:

{resume_text}

Return ONLY valid JSON.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        text = (response.text or "").strip()

        if not text:
            raise ValueError("Empty response from Gemini")

        # Remove markdown fences if Gemini adds them
        if text.startswith("```json"):
            text = text[len("```json"):].strip()

        elif text.startswith("```"):
            text = text[len("```"):].strip()

        if text.endswith("```"):
            text = text[:-3].strip()

        return text


    except Exception as e:
        import traceback

        traceback.print_exc()
        print("Gemini Error:", e)

        return """
{
    "ats_score": 0,

    "overall_rating": "Unknown",

    "experience_level": "Unknown",

    "resume_title": "Resume Analysis",

    "resume_summary": "Unable to analyze the resume.",

    "strengths": [],

    "weaknesses": [],

    "missing_skills": [],

    "recommended_roles": [],

    "interview_questions": [],

    "learning_roadmap": [],

    "suggestions": [
        "Gemini API failed. Please try again later."
    ]
}
"""