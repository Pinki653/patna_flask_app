from flask import Flask, render_template, request

app = Flask(__name__)

# Weighted symptoms for accuracy
SYMPTOM_WEIGHTS = {
    "fever": 2,
    "cough": 2,
    "fatigue": 1,
    "loss_of_smell": 3,
    "breathing": 4,
    "sore_throat": 1,
    "headache": 1,
    "chest_pain": 3
}

def calculate_risk(symptoms):
    score = sum(SYMPTOM_WEIGHTS.get(s, 0) for s in symptoms)
    if score >= 8:
        return {"level": "High", "color": "danger", "advice": "Seek medical help immediately.", "score": score}
    elif score >= 4:
        return {"level": "Moderate", "color": "warning", "advice": "Monitor symptoms and get tested.", "score": score}
    else:
        return {"level": "Low", "color": "success", "advice": "No major symptoms. Stay safe!", "score": score}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')
        result = calculate_risk(symptoms)
        result['symptoms'] = symptoms
    return render_template('covid.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
