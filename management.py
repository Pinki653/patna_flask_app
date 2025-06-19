from flask import Flask, render_template, request, redirect, session
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretkey'

# Sample user database with roles
USERS = {
    "doctor1": {"password": "pass123", "role": "doctor"},
    "staff1": {"password": "pass456", "role": "staff"},
    "admin": {"password": "admin123", "role": "admin"}
}

# Sample data
prescriptions = []
doctors = [{"name": "Dr. Smith", "specialization": "Cardiology", "timing": "10AM - 2PM"}]
staff = [{"name": "Alice", "role": "Nurse", "attendance": "Present", "salary": 50000}]

# Authentication decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username]['password'] == password:
            session['user'] = username
            session['role'] = USERS[username]['role']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', doctors=doctors, staff=staff, prescriptions=prescriptions)

@app.route('/doctors', methods=['GET', 'POST'])
@login_required
def manage_doctors():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        timing = request.form['timing']
        doctors.append({'name': name, 'specialization': specialization, 'timing': timing})
    return render_template('doctors.html', doctors=doctors)

@app.route('/staff', methods=['GET', 'POST'])
@login_required
def manage_staff():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        attendance = request.form['attendance']
        salary = request.form['salary']
        staff.append({'name': name, 'role': role, 'attendance': attendance, 'salary': salary})
    return render_template('staff.html', staff=staff)

@app.route('/prescriptions', methods=['GET', 'POST'])
@login_required
def manage_prescriptions():
    if session.get('role') != 'doctor':
        return "Unauthorized", 403
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        details = request.form['details']
        prescriptions.append({
            'patient_name': patient_name,
            'doctor_name': doctor_name,
            'details': details,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return render_template('prescriptions.html', prescriptions=prescriptions)

if __name__ == '__main__':
    app.run(debug=True)
