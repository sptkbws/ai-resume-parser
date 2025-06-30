import re
import spacy

nlp = spacy.load("en_core_web_sm")

# ✅ Updated Skill List (expand as needed)
SKILL_DB = [
    "python", "java", "sql", "c++", "html", "css", "javascript",
    "git", "github", "matlab", "vhdl", "xilinx vivado", "arduino",
    "visual studio code", "jira", "postman", "mysql", "linux", "bash",
    "gdb", "autocad", "wireshark", "vmware", "junit", "owasp zap", "lucidchart"
]

def extract_name(text):
    lines = text.strip().split("\n")[:10]  # Top 10 lines only
    ignore_keywords = ['email', 'phone', 'linkedin', 'github', 'engineer', 'programmer', 'technician']
    
    for line in lines:
        clean_line = line.strip()
        if 2 <= len(clean_line.split()) <= 4:  # Likely name = 2-4 words
            lower_line = clean_line.lower()
            if not any(keyword in lower_line for keyword in ignore_keywords):
                if clean_line.isupper() or clean_line.istitle():  # Formatting check
                    return clean_line
    return "Not Found"

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group().strip() if match else "Not Found"

def extract_phone(text):
    match = re.search(r"(\+?\d{1,3}[-\s]?)?(\(?\d{3,5}\)?[-\s]?)?\d{3,5}[-\s]?\d{3,5}", text)
    return match.group().strip() if match else "Not Found"

def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in SKILL_DB:
        if skill in text_lower:
            found.append(skill)
    return list(set(found)) if found else ["Not Found"]

def extract_entities(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }
