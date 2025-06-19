from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patients.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    treatment = db.Column(db.String(500), nullable=False)
    room_no = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('report.html')

@app.route('/admit_patient', methods=['POST'])
def admit_patient():
    data = request.get_json()
    name, age, diagnosis, treatment = data["name"], data["age"], data["diagnosis"], data["treatment"]
    
    # Check if patient already exists
    existing_patient = Patient.query.filter_by(name=name).first()
    if existing_patient:
        return jsonify({"message": f"Patient {name} is already admitted!"}), 400

    new_patient = Patient(name=name, age=age, diagnosis=diagnosis, treatment=treatment,
                          room_no=random.randint(100, 500), floor=random.randint(1, 5))
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": f"Patient {name} admitted successfully!"})

@app.route('/get_report')
def get_report():
    name = request.args.get("name", "").strip()
    patient = Patient.query.filter_by(name=name).first()
    
    if not patient:
        return jsonify({"error": "Patient not found!"})

    return jsonify({
        "name": patient.name,
        "age": patient.age,
        "diagnosis": patient.diagnosis,
        "treatment": patient.treatment,
        "room_no": patient.room_no,
        "floor": patient.floor
    })

if __name__ == '__main__':
    app.run(debug=True)
