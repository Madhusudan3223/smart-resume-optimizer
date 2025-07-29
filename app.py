# app.py

import streamlit as st
import fitz  # PyMuPDF for PDF
import docx
from io import StringIO

st.set_page_config(page_title="Smart Resume Optimizer", layout="wide")
st.title("📄 Smart Resume Optimizer")
st.write("Upload your resume and job description to get AI-powered keyword feedback.")

# PDF extractor
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# DOCX extractor
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# File Upload UI
resume_file = st.file_uploader("📤 Upload Resume (.pdf or .docx)", type=["pdf", "docx"])
jd_file = st.file_uploader("📥 Upload Job Description (.txt)", type=["txt"])

if resume_file and jd_file:
    # Extract resume text
    if resume_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(resume_file)
    elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(resume_file)
    else:
        resume_text = ""

    # Extract job description text
    jd_text = StringIO(jd_file.read().decode()).read()

    st.subheader("✅ Resume Preview")
    st.text_area("Extracted Resume Text", resume_text[:1500], height=200)

    st.subheader("✅ Job Description Preview")
    st.text_area("Extracted JD Text", jd_text[:1500], height=200)

    st.success("✅ Files processed successfully. Running keyword matching...")

    # --- Keyword Matching Logic ---
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    matched_keywords = resume_words & jd_words
    missing_keywords = jd_words - resume_words

    st.subheader("🔍 Matched Keywords")
    st.write(", ".join(sorted(matched_keywords)))

    st.subheader("⚠️ Missing Keywords")
    st.write(", ".join(sorted(missing_keywords)))

    st.info("📌 Tip: Try including missing keywords if they're relevant. It can boost ATS score & recruiter match.")
