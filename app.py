import streamlit as st
import re
from PyPDF2 import PdfReader
from io import BytesIO
import docx2txt
from skills_keywords import skills_keywords
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

# Function to extract the candidate's name from the resume
def extract_candidate_name(text):
    try:
        name_pattern = r'\b[A-Z][a-zA-Z]* [A-Z][a-zA-Z]*\b'
        candidate_name = re.search(name_pattern, text)
        return candidate_name.group() if candidate_name else "Name not found"
    except Exception as e:
        return {"error": str(e)}

# Function to extract GitHub link from the resume text
def extract_github_link(text):
    try:
        # Search for GitHub link keywords in the text
        github_keywords = ["github.com/", "https://github.com/"]
        for keyword in github_keywords:
            if keyword in text.lower():
                start_index = text.lower().index(keyword)
                end_index = text.find(" ", start_index)
                github_link = text[start_index:end_index].strip()
                return github_link

        return "GitHub link not found"
    except Exception as e:
        return {"error": str(e)}

# Function to extract the GitHub username from the URL
def extract_username_from_url(github_link):
    parsed_url = urlparse(github_link)
    if parsed_url.netloc == "github.com":
        # Extract the username from the URL path
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) >= 1:
            return path_parts[0]
    return None

# Function to fetch user repositories
def fetch_user_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    try:
        resume_content = uploaded_file.read()
        pdf = PdfReader(BytesIO(resume_content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return {"error": str(e)}

# Function to extract text from a DOCX file
def extract_text_from_docx(uploaded_file):
    try:
        text = docx2txt.process(uploaded_file)
        return text
    except Exception as e:
        return {"error": str(e)}

# Function to extract skills from the resume text
def extract_candidate_skills(text):
    try:
        skills = list(set([skill.lower().capitalize() for skill in skills_keywords if re.search(rf'\b{skill}\b', text, re.IGNORECASE)]))
        return skills
    except Exception as e:
        return {"error": str(e)}

# Function to extract skills from the user-provided job description text
def extract_job_description_skills(job_description_text):
    try:
        skills = list(set([skill.lower().capitalize() for skill in skills_keywords if re.search(rf'\b{skill}\b', job_description_text, re.IGNORECASE)]))
        return skills
    except Exception as e:
        return {"error": str(e)}

# Function to calculate the matching score based on skills
def calculate_matching_score(candidate_skills, job_description_text):
    job_skills = extract_job_description_skills(job_description_text)
    common_skills = list(set(candidate_skills) & set(job_skills))

    if job_skills:
        score = len(common_skills) / len(job_skills)
    else:
        score = 0.0

    return score, common_skills

# Set Streamlit page title and icon
st.set_page_config(
    page_title="Resume and GitHub Analyzer",
    page_icon=":page_with_curl:"
)

# Introduction Section
st.title("Welcome to the Resume Analyzer! made by AMH")

# Create a sidebar for inputs
st.sidebar.title("Resume and GitHub Analyzer")

# Upload Resume Section in Sidebar
st.sidebar.subheader("Step 1: Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF or DOC/DOCX)")

# Enter Job Description Section in Sidebar
st.sidebar.subheader("Step 2: Enter Job Description")
job_description_text = st.sidebar.text_area("Enter the job description")

# Analyze Button in Sidebar
if st.sidebar.button("Analyze"):
    if not uploaded_file or not job_description_text:
        st.warning("Please complete both steps to analyze.")
    else:
        with st.spinner("Analyzing..."):
            # Extract text from the uploaded resume file
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a PDF or DOC/DOCX file.")
                st.stop()

            # Extract GitHub link from the candidate's resume text
            github_link = extract_github_link(resume_text)

            # Calculate the matching score based on skills
            score, common_skills = calculate_matching_score(extract_candidate_skills(resume_text), job_description_text)

            # Left Column (Name, GitHub Link, Common Skills, GitHub Repositories, Technologies)
            st.subheader("Candidate Information")
            col1, col2 = st.columns(2)

            # Candidate Name
            with col1:
                candidate_name = extract_candidate_name(resume_text)
                st.write(f"Name: {candidate_name}")

            # GitHub Link
            with col1:
                if "error" in github_link:
                    st.write(f"Error: {github_link['error']}")
                else:
                    # Check if the link is missing "https://" and add it if necessary
                    if not github_link.startswith("https://"):
                        github_link = "https://" + github_link
                    st.write(f"GitHub: [{github_link}]({github_link})")

            # Common Skills
            with col1:
                st.subheader("Common Skills with Job Description")
                if common_skills:
                    for skill in common_skills:
                        st.write(f"- {skill}")
                else:
                    st.write("No common skills found between the job description and the candidate's skills.")

            

            # GitHub Repositories and Technologies
            with col2:
                st.subheader("GitHub Repositories and Technologies")
                username = extract_username_from_url(github_link)
                if username:
                    user_repositories = fetch_user_repositories(username)
                    if user_repositories:
                        repo_data = {
                            "Repository Name": [],
                            "Technologies Used": []
                        }

                        for repo in user_repositories:
                            repo_name = repo.get("name", "")
                            repo_language = repo.get("language", "")
                            if repo_name:
                                repo_data["Repository Name"].append(repo_name)
                            if repo_language:
                                repo_data["Technologies Used"].append(repo_language)

                        # Ensure both lists have the same length
                        max_length = max(len(repo_data["Repository Name"]), len(repo_data["Technologies Used"]))
                        repo_data["Repository Name"] += [""] * (max_length - len(repo_data["Repository Name"]))
                        repo_data["Technologies Used"] += [""] * (max_length - len(repo_data["Technologies Used"]))

                        # Create a DataFrame for displaying repositories and technologies
                        repo_df = pd.DataFrame(repo_data)

                        st.write(repo_df)
                    else:
                        st.write(f"No repositories found for {github_link}.")
                else:
                    st.write("Invalid GitHub profile link. Please check the link format.")

            # Right Column (Matching Score, All Skills)
            st.subheader("Matching Score and All Skills")
            col3, col4, col5 = st.columns(3)  # Add a third column

            # Matching Score
            with col3:
                score_color = "green" if score >= 0.8 else "orange" if 0.5 <= score < 0.8 else "red"

                # Create a circular progress bar for the matching score
                st.markdown(
                    f'<div style="text-align: center;">'
                    f'<p style="font-size: 16px;">Matching Score</p>'
                    f'<div style="border-radius: 50%; background-color: {score_color}; width: 80px; height: 80px; margin: 0 auto;">'
                    f'<p style="font-size: 24px; color: white; line-height: 80px;">{int(score * 100)}%</p>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # All Skills
            with col4:
                st.markdown(
                    f'<div style="text-align: center;">'
                    f'<p style="font-size: 16px;">All Skills</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                extracted_skills = extract_candidate_skills(resume_text)
                if extracted_skills:
                    skills_text = ", ".join(extracted_skills)
                else:
                    skills_text = "No skills found in the resume."

                st.markdown(
                    f'<p style="font-size: 14px;">{skills_text}</p>',
                    unsafe_allow_html=True
                )
