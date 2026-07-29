import json
import textwrap

import PyPDF2

from django.shortcuts import render, redirect
from django.http import HttpResponse

from reportlab.pdfgen import canvas

from .gemini import analyze_resume


def home(request):

    if request.method == "POST":

        resume = request.FILES.get("resume")

        if not resume:
            return render(
                request,
                "home.html",
                {"error": "Please upload a resume file."}
            )

        try:
            reader = PyPDF2.PdfReader(resume)

            extracted_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text

        except Exception:
            return render(
                request,
                "home.html",
                {"error": "Couldn't read that file. Please upload a valid PDF."}
            )

        if not extracted_text.strip():
            return render(
                request,
                "home.html",
                {"error": "No readable text found in this PDF. Avoid scanned/image-only resumes."}
            )

        ai_text = analyze_resume(extracted_text)

        print("========== GEMINI RESPONSE ==========")
        print(ai_text)
        print("=====================================")

        ai_text = (
            ai_text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            response = json.loads(ai_text)

        except Exception:
            response = {
                "ats_score": 0,
                "resume_summary": "Unable to analyze resume.",
                "strengths": [],
                "weaknesses": [],
                "missing_skills": [],
                "recommended_roles": [],
                "interview_questions": [],
                "learning_roadmap": [],
                "suggestions": [
                    "AI returned an invalid response."
                ]
            }

        request.session["report"] = response

        return redirect("result")

    return render(request, "home.html")

def result(request):

    response = request.session.get("report")

    if not response:
        return redirect("home")

    return render(
        request,
        "result.html",
        {
            "response": response
        }
    )


def _draw_wrapped(p, x, y, text, width_chars=90, line_height=18, bottom_margin=60):
    """
    Draw text wrapped to multiple lines so nothing runs off the page edge.
    Returns the updated y position, handling page breaks as needed.
    """
    wrapped_lines = textwrap.wrap(text, width=width_chars) or [""]

    for line in wrapped_lines:

        if y < bottom_margin:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 800

        p.drawString(x, y, line)
        y -= line_height

    return y


def download_pdf(request):

    response = request.session.get("report")

    if not response:
        return HttpResponse("No report available.")

    pdf = HttpResponse(content_type="application/pdf")

    pdf["Content-Disposition"] = 'attachment; filename="NextHire_Report.pdf"'

    p = canvas.Canvas(pdf)

    y = 800

    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y, "NextHire AI Resume Report")

    y -= 40

    p.setFont("Helvetica", 12)

    p.drawString(50, y, f"ATS Score: {response.get('ats_score', 0)}%")
    y -= 30

    p.drawString(50, y, "Resume Summary")
    y -= 20

    summary = response.get("resume_summary", "")
    y = _draw_wrapped(p, 60, y, summary, width_chars=85)

    sections = [

        ("Strengths", "strengths"),

        ("Weaknesses", "weaknesses"),

        ("Missing Skills", "missing_skills"),

        ("Recommended Roles", "recommended_roles"),

        ("Interview Questions", "interview_questions"),

        ("Learning Roadmap", "learning_roadmap"),

        ("Suggestions", "suggestions"),

    ]

    for title, key in sections:

        y -= 15

        if y < 60:
            p.showPage()
            y = 800

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, title)
        y -= 20

        p.setFont("Helvetica", 12)

        for item in response.get(key, []):
            y = _draw_wrapped(p, 60, y, f"• {item}", width_chars=85)

    p.save()

    return pdf



