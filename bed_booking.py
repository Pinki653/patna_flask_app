from flask import Blueprint, render_template, request
import csv
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create the blueprint
bed_booking_bp = Blueprint('bed_booking', __name__)

# Generate random room and floor
def generate_room():
    room = random.randint(100, 500)
    floor = random.choice(['Ground', '1st', '2nd', '3rd', '4th'])
    return room, floor

# Bed type charges
def get_charges(bed_type):
    charges = {
        'General': 1000,
        'Private': 2500,
        'ICU': 5000
    }
    return charges.get(bed_type, 0)

# Send email confirmation
def send_email(to_email, subject, body):
    sender_email = "your_email@gmail.com"          # Replace with your email
    sender_password = "your_app_password_here"     # Use Gmail App Password

    msg = MIMEMultipart()
    msg['From'] = "Care Point Hospital"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email failed:", e)

# Route to book bed
@bed_booking_bp.route('/book-bed', methods=['GET', 'POST'])
def book_bed():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        department = request.form['department']
        bed_type = request.form['bed_type']
        email = request.form['email']

        room, floor = generate_room()
        charges = get_charges(bed_type)

        # Save booking to CSV
        file_exists = os.path.isfile('bed_bookings.csv')
        with open('bed_bookings.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Age', 'Gender', 'Department', 'Bed Type', 'Email', 'Room', 'Floor', 'Charges'])
            writer.writerow([name, age, gender, department, bed_type, email, room, floor, charges])

        # Email content
        email_body = f"""
        <h2>Care Point Hospital - Bed Booking Confirmation</h2>
        <p>Dear {name},</p>
        <p>Your bed has been booked successfully.</p>
        <ul>
          <li><strong>Department:</strong> {department}</li>
          <li><strong>Bed Type:</strong> {bed_type}</li>
          <li><strong>Room Number:</strong> {room}</li>
          <li><strong>Floor:</strong> {floor}</li>
          <li><strong>Charges:</strong> ₹{charges}/day</li>
        </ul>
        <p>Thank you for choosing Care Point Hospital!</p>
        """
        send_email(email, "Care Point Hospital - Bed Booking Confirmation", email_body)

        return render_template('bill_slip.html', name=name, age=age, gender=gender,
                               department=department, bed_type=bed_type, email=email,
                               room=room, floor=floor, charges=charges)

    return render_template('book_bed.html')
