# 📄 CV Analyzer and Skill Matcher 🚀  

An innovative tool that **extracts and analyzes CV data**, matches candidate skills with job descriptions, and retrieves GitHub repositories for an enhanced recruitment experience.

## ✨ Features  

### 🔍 **CV Information Extraction**  
- Supports **PDF** and **DOCX** file formats.  
- Extracts:  
  - 📛 **Candidate Name** using regular expressions.  
  - 🔗 **GitHub Link** embedded in the CV.  

---

### 🛠️ **Skill Analysis**  
- **Compares skills** listed in the candidate's CV with those from the job description.  
- Calculates a **matching score** based on shared skills.  
- Displays:  
  - ✅ **Common Skills** between the CV and job requirements.  
  - 📝 **All Skills** extracted from the CV.  

---

### 🧑‍💻 **GitHub Profile Analysis**  
- Fetches **public repositories** from the candidate's GitHub profile using the **GitHub API**.  
- Identifies the primary **technologies** (programming languages) for each repository.  
- Displays results in an **interactive table**.  

---

### 🎨 **Streamlit Interactive UI**  
- Clean, organized, and responsive interface using **Streamlit**.  
- Key Features:  
  - 📊 **Circular Matching Score** visualization (Green: High, Orange: Medium, Red: Low).  
  - 🗂️ **Interactive Tables** displaying repositories and technologies.  
  - 🖥️ **Well-organized layout** for CV, skills, and GitHub information.

---

## 🚀 **How It Works**  

1. **Upload the CV** (PDF/DOCX) via the Streamlit interface.  
2. The system extracts candidate details:  
   - Name  
   - GitHub profile link  
3. **Provide the job description** to extract relevant skills.  
4. **Skill Matching**:  
   - The tool compares extracted skills to job requirements and calculates a match score.  
5. **GitHub Analysis**:  
   - Fetches repositories and displays technologies in a table.  

---

## 📦 **Installation**  

1. Clone the repository:  
   ```bash
   git clone https://github.com/HAMMOUDAmustaphaahmed/Resume_Checker.git
   cd your-repository  
   pip install -r requirements.txt  
   streamlit run app.py  
