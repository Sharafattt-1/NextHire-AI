# NextHire AI - AI Resume Analyzer

NextHire AI is an AI-powered resume analysis web application designed to help job seekers improve their resumes and increase their chances of getting better career opportunities. The project uses artificial intelligence to analyze resume content, identify important skills, evaluate keywords, and provide useful suggestions for improving the overall quality of a resume. The main purpose of this application is to make the resume review process faster, smarter, and more accessible by providing automated feedback instead of requiring manual analysis.

The application allows users to upload their resumes and receive AI-generated insights about their resume structure, skills, strengths, weaknesses, and possible improvements. It can help users understand whether their resume properly represents their abilities and what changes can make it more effective for recruiters and hiring systems. This project can be useful for students, fresh graduates, and professionals who want to optimize their resumes before applying for jobs.

NextHire AI is built using Python and Django for backend development, along with HTML, CSS, and JavaScript for creating the user interface. The project integrates the Gemini AI API to provide intelligent resume analysis and generate meaningful recommendations. SQLite is used as the database for managing application data. Environment variables are used to securely store sensitive information such as API keys and other configuration details.

## Features

- AI-powered resume analysis
- Resume upload and processing
- Extraction and evaluation of skills and keywords
- AI-generated suggestions for improving resumes
- User-friendly interface
- Automated feedback for resume quality improvement
- Secure handling of API keys using environment variables

## Installation and Setup

To run this project locally, first clone the repository to your system. After downloading the project, create a virtual environment and activate it. Install all required dependencies using the requirements.txt file. Create a `.env` file in the project directory and add the required API keys and environment variables. After completing the setup, run the Django development server using the command `python manage.py runserver` and open the provided local URL in your browser.

## Project Usage

Users can upload their resume files through the application, after which the system processes the resume and uses AI to analyze the content. The application provides feedback that helps users improve their resumes by focusing on relevant skills, better formatting, and stronger descriptions of their experience.

## Future Improvements

Future updates may include adding user authentication, saving previous resume analyses, job description matching, advanced resume scoring, and personalized career recommendations.

This project demonstrates the practical implementation of artificial intelligence in career assistance and shows how AI can be integrated into real-world web applications to solve practical problems.