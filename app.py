import streamlit as st
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer (Advanced)")

# 🔥 TECH KEYWORDS (to avoid junk words)
TECH_KEYWORDS = {
    "python", "sql", "excel", "power", "bi", "tableau",
    "pandas", "numpy", "machine", "learning",
    "data", "analysis", "dashboard", "visualization"
}

# 🔹 Clean words (ONLY meaningful ones)
def clean_words(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return {w for w in words if w in TECH_KEYWORDS}


# 🔹 Inputs
job_role = st.text_input("🎯 Enter Job Role (optional)")
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
jd_text = st.text_area("📋 Paste Job Description (optional)")


# 🔹 MAIN
if uploaded_file is not None:

    # 🔹 Extract text
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    text_lower = text.lower()

    st.subheader("📄 Resume Preview")
    st.write(text[:800])

    st.divider()

    # 🔹 Skills
    skills = [
        "python", "machine learning", "sql", "excel",
        "power bi", "tableau", "pandas", "numpy"
    ]

    found_skills = [s for s in skills if s in text_lower]
    missing_skills = [s for s in skills if s not in found_skills]

    # 🔹 Sections
    sections = {
        "education": ["education", "degree", "college"],
        "experience": ["experience", "internship", "work"],
        "projects": ["project"],
        "skills": ["skills"]
    }

    section_present = {}
    section_score = 0

    for sec, keywords in sections.items():
        found = any(word in text_lower for word in keywords)
        section_present[sec] = found
        if found:
            section_score += 2

    # 🔹 Score
    skill_score = min(len(found_skills), 5)
    total_score = min(section_score + skill_score, 10)
    coverage = int((len(found_skills) / len(skills)) * 100)

    # 🔹 UI
    col1, col2 = st.columns(2)
    col1.metric("📊 Resume Score", f"{total_score}/10")
    col2.metric("📈 Skill Coverage", f"{coverage}%")

    st.progress(total_score / 10)

    st.divider()

    # 🔹 Skills display
    st.subheader("🧠 Skills Detected")
    if found_skills:
        st.success(", ".join(found_skills))
    else:
        st.warning("No skills detected")

    st.subheader("❌ Missing Skills")
    if missing_skills:
        st.warning(", ".join(missing_skills))
    else:
        st.success("All important skills present")

    st.divider()

    # 🔹 Sections
    st.subheader("📂 Resume Sections")
    for sec, present in section_present.items():
        if present:
            st.markdown(f"✅ **{sec.title()}**")
        else:
            st.markdown(f"❌ **{sec.title()} missing**")

    st.divider()

    # 🔹 JOB MATCH
    job_map = {
        "data analyst": ["sql", "excel", "power bi", "tableau"],
        "ml engineer": ["python", "machine learning", "pandas"],
        "data scientist": ["python", "machine learning", "statistics"]
    }

    match_score = None
    matched_role = None

    if job_role:
        role = job_role.strip().lower()

        for key in job_map:
            if key in role:
                matched_role = key
                break

        if matched_role:
            required = job_map[matched_role]
            match = sum(1 for s in required if s in text_lower)
            match_score = int((match / len(required)) * 100)

            st.subheader("🎯 Job Match Score")
            st.success(f"{match_score}% match for {matched_role.title()}")
        else:
            st.warning("Role not supported yet")

    st.divider()

    # 🔥 JD MATCH (CLEANED)
    jd_match_percent = None
    missing_keywords = []

    if jd_text:
        st.subheader("📋 JD Match Analysis")

        jd_words = clean_words(jd_text)
        resume_words = clean_words(text)

        common = resume_words.intersection(jd_words)

        if len(jd_words) > 0:
            jd_match_percent = int((len(common) / len(jd_words)) * 100)
        else:
            jd_match_percent = 0

        st.success(f"{jd_match_percent}% match with job description")

        missing_keywords = jd_words - resume_words

        st.subheader("🚨 Missing JD Keywords")

        if missing_keywords:
            st.warning(", ".join(list(missing_keywords)[:15]))
        else:
            st.success("No major keywords missing")

    st.divider()

    # 🔹 Feedback
    st.subheader("💡 Smart Feedback")

    feedback = []

    if total_score >= 8:
        feedback.append("Strong resume with solid structure.")
    elif total_score >= 5:
        feedback.append("Decent resume but needs improvement.")
    else:
        feedback.append("Resume needs major improvements.")

    if not section_present["projects"]:
        feedback.append("Add 2–3 strong projects.")

    if not section_present["experience"]:
        feedback.append("Include internship/work experience.")

    if len(found_skills) < 4:
        feedback.append("Add more technical skills.")

    if missing_skills:
        feedback.append(f"Consider adding: {', '.join(missing_skills[:3])}")

    for f in feedback:
        st.markdown(f"- {f}")

    st.divider()

    # 🔹 Report
    report = f"""
AI Resume Analysis Report

Score: {total_score}/10
Coverage: {coverage}%

Skills Found:
{', '.join(found_skills) if found_skills else 'None'}

Missing Skills:
{', '.join(missing_skills) if missing_skills else 'None'}

Sections Present:
{', '.join([k for k,v in section_present.items() if v])}

Feedback:
{chr(10).join(['- ' + f for f in feedback])}
"""

    if match_score is not None:
        report += f"\nJob Match Score: {match_score}% for {matched_role.title()}"

    if jd_match_percent is not None:
        report += f"\nJD Match Score: {jd_match_percent}%"

    st.download_button("📥 Download Report", report, "resume_report.txt")