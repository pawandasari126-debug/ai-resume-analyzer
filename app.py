import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer (Final Version)")

# 🔥 TECH KEYWORDS
TECH_KEYWORDS = {
    "python", "sql", "excel", "power", "bi", "tableau",
    "pandas", "numpy", "machine", "learning",
    "data", "analysis", "dashboard", "visualization"
}

# 🔹 Clean words
def clean_words(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return {w for w in words if w in TECH_KEYWORDS}

# 🔹 Highlight function
def highlight_text(text, found, missing):
    highlighted = text

    for word in found:
        highlighted = re.sub(
            rf"\b({word})\b",
            r"<span style='color:green;font-weight:bold'>\1</span>",
            highlighted,
            flags=re.IGNORECASE
        )

    for word in missing:
        highlighted = re.sub(
            rf"\b({word})\b",
            r"<span style='color:red;font-weight:bold'>\1</span>",
            highlighted,
            flags=re.IGNORECASE
        )

    return highlighted


# 🔹 Inputs
job_role = st.text_input("🎯 Enter Job Role (optional)")
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

st.subheader("📋 Job Description Input")
jd_text = st.text_area("Paste Job Description")

jd_pdf = st.file_uploader("OR Upload JD PDF", type=["pdf"])

# 🔹 Extract JD from PDF if uploaded
if jd_pdf is not None:
    jd_reader = PdfReader(jd_pdf)
    jd_text = ""
    for page in jd_reader.pages:
        jd_text += page.extract_text() or ""

# 🔹 MAIN
if uploaded_file is not None:

    # 🔹 Extract resume
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    text_lower = text.lower()

    st.subheader("📄 Resume Preview")
    st.write(text[:500])

    st.divider()

    # 🔹 Skills list
    skills = [
        "python", "machine learning", "sql", "excel",
        "power bi", "tableau", "pandas", "numpy"
    ]

    found_skills = [s for s in skills if s in text_lower]
    missing_skills = [s for s in skills if s not in found_skills]

    # 🔹 Score
    total_score = min(len(found_skills), 10)
    coverage = int((len(found_skills) / len(skills)) * 100)

    col1, col2 = st.columns(2)
    col1.metric("📊 Resume Score", f"{total_score}/10")
    col2.metric("📈 Skill Coverage", f"{coverage}%")

    st.progress(total_score / 10)

    st.divider()

    # 🔹 Skills display
    st.subheader("🧠 Skills Detected")
    st.success(", ".join(found_skills) if found_skills else "None")

    st.subheader("❌ Missing Skills")
    st.warning(", ".join(missing_skills) if missing_skills else "None")

    st.divider()

    # 🔥 JD MATCH
    if jd_text:
        st.subheader("📋 JD Match Analysis")

        jd_words = clean_words(jd_text)
        resume_words = clean_words(text)

        common = resume_words.intersection(jd_words)

        match_percent = int((len(common) / len(jd_words)) * 100) if jd_words else 0

        st.success(f"{match_percent}% match with job description")

        missing_keywords = jd_words - resume_words

        st.subheader("🚨 Missing JD Keywords")
        st.warning(", ".join(list(missing_keywords)[:15]) if missing_keywords else "None")

        st.divider()

        # 🔥 Highlight Resume
        st.subheader("📝 Highlighted Resume")

        highlighted = highlight_text(text, found_skills, missing_keywords)

        st.markdown(highlighted, unsafe_allow_html=True)

    st.divider()

    # 🔹 Report
    report = f"""
AI Resume Analysis Report

Score: {total_score}/10
Coverage: {coverage}%

Skills Found:
{', '.join(found_skills)}

Missing Skills:
{', '.join(missing_skills)}

"""

    if jd_text:
        report += f"\nJD Match Score: {match_percent}%"

    st.download_button("📥 Download Report", report, "resume_report.txt")