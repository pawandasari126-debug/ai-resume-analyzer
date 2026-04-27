import streamlit as st
from PyPDF2 import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get insights")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:

    import pdfplumber

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    st.subheader("📄 Extracted Text")
    st.write(text[:1000])

    # 🔹 Skills
    skills = [
        "python", "machine learning", "data science", "sql",
        "excel", "power bi", "tableau", "deep learning",
        "nlp", "pandas", "numpy", "streamlit"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    st.subheader("🧠 Skills Detected")

    if found_skills:
        st.success(", ".join(found_skills))
    else:
        st.warning("No relevant skills found")

    # 🔹 SCORE
    score = 0

    if len(found_skills) >= 5:
        score += 5
    elif len(found_skills) >= 3:
        score += 3
    else:
        score += 1

    if len(text) > 1000:
        score += 3
    elif len(text) > 500:
        score += 2
    else:
        score += 1

    score = min(score, 10)

    st.subheader("📊 Resume Score")
    st.success(f"{score} / 10")

    # 🔹 Suggestions
    st.subheader("💡 Suggestions")

    if score >= 8:
        st.success("Great resume! Just refine formatting and clarity.")
    elif score >= 5:
        st.warning("Good resume, but add more projects and details.")
    else:
        st.error("Improve resume by adding skills, projects, and experience.")

# 🔹 Generate PDF Report
    def create_pdf(text, skills, score):
        file_path = "resume_report.pdf"

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        content = []

        content.append(Paragraph("AI Resume Report", styles['Title']))
        content.append(Paragraph(f"Score: {score}/10", styles['Normal']))
        content.append(Paragraph(f"Skills: {', '.join(skills)}", styles['Normal']))
        content.append(Paragraph(" ", styles['Normal']))
        content.append(Paragraph("Resume Content:", styles['Heading2']))
        content.append(Paragraph(text[:1000], styles['Normal']))

        doc.build(content)

        return file_path


    pdf_file = create_pdf(text, found_skills, score)

    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download Report", f, file_name="resume_report.pdf")