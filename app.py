from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for Flask-WTF forms

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')  # Default MongoDB port
db = client['covid-detection-db']
collection = db['submissions']

# Define COVID Symptoms
COVID_SYMPTOMS = [
    'fever',
    'cough',
    'fatigue',
    'loss of taste or smell',
    'difficulty breathing',
    'sore throat',
    'headache',
    'muscle pain',
    'chills',
    'nausea or vomiting',
    'diarrhea'
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        contact = request.form.get('contact')
        email = request.form.get('email')
        # Collect symptoms - assuming checkboxes with name='symptoms'
        symptoms = request.form.getlist('symptoms')

        # Current timestamp
        submission_time = datetime.utcnow()

        # Prepare the document to insert
        submission = {
            'name': name,
            'age': age,
            'gender': gender,
            'contact': contact,
            'email': email,
            'symptoms': symptoms,
            'submission_time': submission_time
        }

        # Insert into MongoDB
        collection.insert_one(submission)

        # Analyze symptoms
        covid_likelihood = analyze_symptoms(symptoms)

        return render_template('result.html', name=name, likelihood=covid_likelihood)

    return render_template('form.html', symptoms=COVID_SYMPTOMS)

# def analyze_symptoms(symptoms):
#     # Simple rule-based logic
#     # For example, if user has 3 or more critical symptoms, high likelihood
#     # Define critical symptoms
#     critical_symptoms = ['fever', 'cough', 'difficulty breathing']

#     matched_critical = set(symptoms).intersection(set(critical_symptoms))
#     matched_total = len(symptoms)

#     if len(matched_critical) >= 2:
#         return 'High likelihood of COVID-19. Please consult a healthcare professional.'
#     elif len(matched_critical) == 1 and matched_total >= 3:
#         return 'Moderate likelihood of COVID-19. Monitor your symptoms closely.'
#     else:
#         return 'Low likelihood of COVID-19. Continue to follow safety guidelines.'

def analyze_symptoms(symptoms):
    # Define symptom weights
    symptom_weights = {
        'fever': 3,
        'cough': 3,
        'fatigue': 2,
        'loss of taste or smell': 4,
        'difficulty breathing': 4,
        'sore throat': 2,
        'headache': 1,
        'muscle pain': 2,
        'chills': 2,
        'nausea or vomiting': 1,
        'diarrhea': 1
    }

    total_score = 0
    for symptom in symptoms:
        total_score += symptom_weights.get(symptom, 0)

    # Define thresholds
    if total_score >= 10:
        return 'High likelihood of COVID-19. Please consult a healthcare professional immediately.'
    elif 6 <= total_score < 10:
        return 'Moderate likelihood of COVID-19. Monitor your symptoms closely and consider getting tested.'
    else:
        return 'Low likelihood of COVID-19. Continue to follow safety guidelines.'


if __name__ == '__main__':
    app.run(debug=True)
