📄 CV Analyzer and Skill Matcher 🚀
An innovative tool that extracts and analyzes CV data, matches candidate skills with job descriptions, and retrieves GitHub repositories for an enhanced recruitment experience.

✨ Features
🔍 CV Information Extraction
Supports PDF and DOCX file formats.
Extracts:
📛 Candidate Name using regular expressions.
🔗 GitHub Link embedded in the CV.
🛠️ Skill Analysis
Compares skills listed in the candidate's CV with those from the job description.
Calculates a matching score based on shared skills.
Displays:
✅ Common Skills between the CV and job requirements.
📝 All Skills extracted from the CV.
🧑‍💻 GitHub Profile Analysis
Fetches public repositories from the candidate's GitHub profile using the GitHub API.
Identifies the primary technologies (programming languages) for each repository.
Displays results in an interactive table.
🎨 Streamlit Interactive UI
Clean, organized, and responsive interface using Streamlit.
Key Features:
📊 Circular Matching Score visualization (Green: High, Orange: Medium, Red: Low).
🗂️ Interactive Tables displaying repositories and technologies.
🖥️ Well-organized layout for CV, skills, and GitHub information.
🚀 How It Works
Upload the CV (PDF/DOCX) via the Streamlit interface.
The system extracts candidate details:
Name
GitHub profile link
Provide the job description to extract relevant skills.
Skill Matching:
The tool compares extracted skills to job requirements and calculates a match score.
GitHub Analysis:
Fetches repositories and displays technologies in a table.
📦 Installation
Clone the repository:

bash
Copier le code
git clone https://github.com/your-repository-url.git  
cd your-repository  
Install required dependencies:

bash
Copier le code
pip install -r requirements.txt  
Run the Streamlit app:

bash
Copier le code
streamlit run app.py  
🛠️ Tech Stack
Technology	Description
Python	Backend processing and logic
Streamlit	Interactive UI and user interface
GitHub API	Fetching repositories and technologies
Regex	Candidate name and link extraction
Pandas	Data analysis and table generation
🎥 Demo

🤝 Contributions
Contributions are welcome! Please submit a pull request or open an issue for any improvements or feature suggestions.

⭐ Acknowledgements
Special thanks to the open-source community and the libraries that made this project possible:

Streamlit
Pandas
GitHub API
🚀 Ready to Streamline Recruitment?
Start matching CVs to job descriptions and analyzing GitHub profiles now!
