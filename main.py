import streamlit as st
import io
import os
from openai import OpenAI
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer",page_icon="📄",layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload  your resume (PDF of TXT)",type=["pdf","txt"])

job_role = st.text_input("Enter te job role your targeting(optional)")

analyze = st.button("Analyze Resume")

def create_pdf(text):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesizr=letter)
    width, height = letter

    lines = text.split('\n')
    y = height - 50
    for line in lines:
        if y < 50:
            p.showPage()
            y = height - 50
            p.drawString(40, y, line[:110])
            y -= 15
    p.save()
    buffer.seek(0)
    return buffer        

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
        return text
    
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:    
        file_content = extract_text_from_file(uploaded_file)

        if not  file_content.strip():
            st.error("File does not have any content...")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        1.Content clarity and impact
        2.Skills presentation
        3.Experience descriptions
        4.Specific improvements for{job_role if job_role else'general job application'}
        5.Rating out of 10
        

Resume contents;
{file_content}

Please provide your analysis in a clear,structured format with specific recommendations."""
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role":"user","content":prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)

        feedback_text = response.choices[0].message.content
        pdf_file = create_pdf(feedback_text)

        st.download_button(
            label="📥 Download Feedback as PDF",
            data=pdf_file,
            file_name="resume_feedback.pdf",
            mime="application/pdf"
        )
        9
    except Exception as e:
        st.error(f"An error occured:{str(e)}")





