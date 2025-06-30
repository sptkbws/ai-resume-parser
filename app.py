import os
import base64
import streamlit as st

from matcher.rank_resumes import rank_resumes_against_jd
from extract_text import extract_resume_text
from extract_entities import extract_entities
from predict_role import predict_job_role

from utils.report_generator import generate_pdf_report
from utils.email_sender import send_email
from utils.job_matcher import get_mock_job_matches

# 🔧 Setup page
st.set_page_config(page_title="AI Resume Parser", page_icon="📄", layout="centered")

# 🎨 Custom CSS
st.markdown("""
    <style>
    .reportview-container .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 16px;
    }
    .stFileUploader label {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 🏷️ App Header
st.title("📄 AI Resume Parser & Recommender")
st.caption("Built with ❤️ using NLP, BERT & Streamlit")

# 📁 Setup folder
UPLOAD_DIR = "resumes_uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 📝 JD Input
job_description = st.text_area("🧾 Paste the Job Description here", height=200)

# 📤 Upload resumes
uploaded_files = st.file_uploader("📤 Upload Resumes (PDF or DOCX)", accept_multiple_files=True)

# 🎛️ Sidebar filters
st.sidebar.header("🛠️ Filters & Settings")
top_n = st.sidebar.slider("Top N Resumes", min_value=1, max_value=20, value=5)
selected_role = st.sidebar.selectbox(
    "🎯 Filter by Predicted Role",
    ["All", "Software Engineer", "Data Scientist", "Data Analyst", "Machine Learning Engineer",
     "AI Researcher", "Cloud Engineer", "DevOps Engineer", "Cybersecurity Analyst", "Backend Developer",
     "Frontend Developer", "Full Stack Developer", "Mobile App Developer", "Android Developer", "iOS Developer",
     "Web Developer", "UI/UX Designer", "QA Tester", "Automation Engineer", "Embedded Systems Engineer",
     "Robotics Engineer", "Control Systems Engineer", "Network Engineer", "Systems Engineer",
     "Site Reliability Engineer", "Technical Support Engineer", "Product Manager", "Project Manager",
     "Business Analyst", "IT Consultant", "Database Administrator", "Cloud Architect",
     "Civil Site Engineer", "Structural Engineer", "Mechanical Design Engineer", "Automotive Engineer",
     "Electrical Design Engineer", "Power Systems Engineer", "Instrumentation Engineer", "VLSI Engineer",
     "RF Engineer", "Telecom Engineer", "Blockchain Developer", "Game Developer",
     "Bioinformatics Analyst", "Biomedical Engineer", "Research Scientist", "Academic/PhD Candidate"]
)

# 🚀 Rank Resumes
if st.button("🔍 Rank Resumes"):
    if not job_description or not uploaded_files:
        st.warning("⚠️ Please provide a JD and upload at least one resume.")
    else:
        st.info("⏳ Processing resumes...")

        # Save resumes
        for file in uploaded_files:
            with open(os.path.join(UPLOAD_DIR, file.name), "wb") as f:
                f.write(file.getbuffer())

        # Rank resumes
        results = rank_resumes_against_jd(UPLOAD_DIR, job_description, top_k=len(uploaded_files))

        rank_data = []
        for filename, score in results[:top_n]:
            full_path = os.path.join(UPLOAD_DIR, filename)
            text = extract_resume_text(full_path)
            entities = extract_entities(text)
            predicted_role = predict_job_role(text)

            # Role filter
            if selected_role != "All" and predicted_role != selected_role:
                continue

            rank_data.append((filename, score, entities.get('name'), entities.get('email'), predicted_role))

        # 📊 Show ranked resumes
        st.subheader("🏆 Filtered & Ranked Resumes")
        if not rank_data:
            st.warning("😕 No matching resumes found with current filters.")
        else:
            for i, (filename, score, name, email, role) in enumerate(rank_data, 1):
                st.markdown(f"### {i}. 📁 {filename}")
                st.write(f"**🔢 Score:** {round(score*100, 2)}%")
                st.write(f"**🙍 Name:** {name or 'N/A'} | 📧 Email: {email or 'N/A'}")
                st.write(f"**🎯 Predicted Role:** {role}")
                st.markdown("---")

            # 📄 Generate PDF report
            report_path = generate_pdf_report(rank_data, job_description)
            with open(report_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                pdf_display = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="resume_ranking_report.pdf">📥 Download Ranking Report (PDF)</a>'
                st.markdown(pdf_display, unsafe_allow_html=True)

            # 📧 Email to HR
            with st.expander("📧 Email Report to HR"):
                hr_email = st.text_input("Enter HR's Email Address")
                if st.button("Send Email to HR"):
                    if hr_email:
                        result = send_email(
                            receiver_email=hr_email,
                            subject="AI Resume Ranking Report",
                            body="Please find attached the ranked resumes based on your Job Description.",
                            attachment_path=report_path
                        )
                        if result is True:
                            st.success("✅ Email sent successfully to HR!")
                        else:
                            st.error(f"❌ Failed to send email: {result}")
                    else:
                        st.warning("⚠️ Please enter a valid email address.")

            # 🔍 JD-based job matching
            with st.expander("🔍 Auto-Match JD to Job Openings"):
                st.info("Here are some job openings matching your JD:")
                job_matches = get_mock_job_matches(job_description)
                for job in job_matches:
                    st.markdown(f"🔗 **[{job['title']}]({job['link']})**")
                    st.write(f"📍 Location: {job['location']}")
                    st.markdown("---")
