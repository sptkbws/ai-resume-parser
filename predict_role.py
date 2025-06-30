import pickle

# Load model and vectorizer
with open("classifier/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("classifier/classifier.pkl", "rb") as f:
    model = pickle.load(f)

def predict_job_role(resume_text):
    """Predict job role given resume text"""
    X_input = vectorizer.transform([resume_text])
    prediction = model.predict(X_input)[0]
    return prediction
