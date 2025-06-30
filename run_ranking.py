from matcher.rank_resumes import rank_resumes_against_jd

job_description = """
Looking for a Python backend developer with experience in REST APIs,
Flask or Django, SQL databases, and Git. Cloud knowledge is a bonus.
"""

resume_folder = "resumes/"
ranked = rank_resumes_against_jd(resume_folder, job_description)

print("\n🏆 Ranked Resumes by JD Relevance:\n")
for i, (name, score) in enumerate(ranked, 1):
    print(f"{i}. {name}  ➤  Score: {round(score * 100, 2)}%")
