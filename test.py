import os
from extract_text import extract_resume_text
from extract_entities import extract_entities
from predict_role import predict_job_role

# 📁 Resume folder path
resume_folder = "resumes/"

# 🔁 Loop through all files
for filename in os.listdir(resume_folder):
    file_path = os.path.join(resume_folder, filename)

    # ✅ Only accept PDF and DOCX
    if filename.lower().endswith((".pdf", ".docx")):
        print(f"\n📄 Processing: {filename}")
        try:
            # STEP 1: Extract resume text
            text = extract_resume_text(file_path)
            print("✅ Resume Text Extracted (First 500 chars):\n")
            print(text[:500])

            # STEP 2: Extract entities
            entities = extract_entities(text)
            print("\n🧠 Extracted Entities:")
            print(f"👤 Name: {entities.get('name')}")
            print(f"📧 Email: {entities.get('email')}")
            print(f"📞 Phone: {entities.get('phone')}")
            print(f"💼 Skills: {', '.join(entities.get('skills', []))}")

            # STEP 3: Predict Job Role
            predicted_role = predict_job_role(text)
            print(f"🔮 Predicted Role: {predicted_role}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
        
        print("--------------------------------------------------")  # separator

    else:
        print(f"⚠️ Skipped unsupported file: {filename}")
