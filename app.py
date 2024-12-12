import streamlit as st
import re
import logging
from PyPDF2 import PdfReader
from io import BytesIO
import docx2txt
from skills_keywords import skills_keywords
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants
GITHUB_KEYWORDS = ["github.com/", "https://github.com/"]
HEADERS = {"Accept": "application/vnd.github.v3+json"}

# Utility Functions
def extract_text_from_file(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            pdf = PdfReader(BytesIO(uploaded_file.read()))
            return "".join(page.extract_text() for page in pdf.pages)
        elif uploaded_file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            return docx2txt.process(uploaded_file)
        else:
            st.error("Unsupported file format. Upload PDF or DOCX.")
            st.stop()
    except Exception as e:
        logging.error(f"Error extracting text: {str(e)}")
        return ""

def extract_pattern(text, pattern, default="Not found"):
    match = re.search(pattern, text)
    return match.group() if match else default

def extract_skills(text):
    return sorted(set(skill.capitalize() for skill in skills_keywords if re.search(rf'\b{skill}\b', text, re.IGNORECASE)))

def extract_github_link(text):
    for keyword in GITHUB_KEYWORDS:
        if keyword in text.lower():
            start_index = text.lower().index(keyword)
            end_index = text.find(" ", start_index)
            return "https://" + text[start_index:end_index].strip()
    return "GitHub link not found"

def fetch_github_repos(username):
    try:
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url, headers=HEADERS)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        logging.error(f"GitHub API error: {str(e)}")
        return []

# Matching Score
def calculate_matching_score(candidate_skills, job_description):
    job_skills = extract_skills(job_description)
    common_skills = set(candidate_skills) & set(job_skills)
    score = len(common_skills) / len(job_skills) if job_skills else 0
    return score, list(common_skills)

# Streamlit App
def main():
    st.set_page_config(page_title="Resume and GitHub Analyzer", page_icon=":page_with_curl:")
    st.title("Resume and GitHub Analyzer")
    st.sidebar.title("Input Section")

    # Inputs
    uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF/DOCX)")
    job_description = st.sidebar.text_area("Enter Job Description")

    if st.sidebar.button("Analyze"):
        if not uploaded_file or not job_description:
            st.warning("Please provide both resume and job description.")
        else:
            with st.spinner("Analyzing..."):
                # Extract Text
                resume_text = extract_text_from_file(uploaded_file)

                # Extract Information
                candidate_name = extract_pattern(resume_text, r'\b[A-Z][a-zA-Z]* [A-Z][a-zA-Z]*\b')
                github_link = extract_github_link(resume_text)
                candidate_skills = extract_skills(resume_text)
                score, common_skills = calculate_matching_score(candidate_skills, job_description)

                # UI: Candidate Info
                st.subheader("Candidate Information")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {candidate_name}")
                    st.write(f"**GitHub Link:** {github_link}")

                # GitHub Repositories
                with col2:
                    st.subheader("GitHub Repositories")
                    username = urlparse(github_link).path.strip("/") if "github" in github_link else None
                    repos = fetch_github_repos(username) if username else []
                    if repos:
                        repo_data = pd.DataFrame({
                            "Repository Name": [repo.get("name", "N/A") for repo in repos],
                            "Language": [repo.get("language", "N/A") for repo in repos]
                        })
                        st.dataframe(repo_data)
                    else:
                        st.write("No repositories found.")

                # Matching Score
                st.subheader("Matching Score")
                score_color = "green" if score >= 0.8 else "orange" if score >= 0.5 else "red"
                st.markdown(f"""
                <div style='text-align:center;'>
                    <div style='border-radius: 50%; background-color:{score_color}; width:100px; height:100px; margin:auto;'>
                        <p style='line-height:100px; color:white; font-size:24px;'>{int(score * 100)}%</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Skills Section
                st.subheader("Skills Analysis")
                st.write(f"**Extracted Skills:** {', '.join(candidate_skills)}")
                st.write(f"**Common Skills with Job:** {', '.join(common_skills) if common_skills else 'None'}")

if __name__ == "__main__":
    main()
