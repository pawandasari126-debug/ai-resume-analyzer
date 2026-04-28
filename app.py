import streamlit as st
from pypdf import PdfReader

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:

    # 🔹 Extract text from PDF
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    # 🔹 Show extracted text (preview)
    st.subheader("📄 Extracted Text")
    st.write(text[:1000])

    # 🔹 Skills list
    skills = [
        "python", "machine learning", "sql", "excel",
        "power bi", "tableau", "pandas", "numpy"
    ]

    # 🔹 Find skills
    found_skills = []
    for skill in skills:
        if skill in text.lower():
            found_skills.append(skill)

    # 🔹 Show skills
    st.subheader("🧠 Skills Detected")
    if found_skills:
        st.success(", ".join(found_skills))
    else:
        st.warning("No skills detected")

    # 🔹 Score
    score = min(len(found_skills), 10)

    st.subheader("📊 Resume Score")
    st.success(f"{score} / 10")

    # 🔹 Suggestions
    st.subheader("💡 Suggestions")

    if score >= 8:
        suggestion = "Great resume! Just refine formatting and clarity."
        st.success(suggestion)
    elif score >= 5:
        suggestion = "Good, but add more skills/projects."
        st.warning(suggestion)
    else:
        suggestion = "Needs improvement. Add more relevant skills and projects."
        st.error(suggestion)

    # 🔹 Create report
    report = f"""
AI Resume Analysis Report

Skills Detected:
{', '.join(found_skills) if found_skills else 'None'}

Score:
{score}/10

Suggestions:
{suggestion}
"""

    # 🔹 Download button
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_report.txt",
        mime="text/plain"
    )