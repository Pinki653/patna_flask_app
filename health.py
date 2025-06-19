from flask import Flask, request, render_template
import csv
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Email Configuration
EMAIL_ADDRESS = 'pinkiastwal929@gmail.com'
EMAIL_PASSWORD = 'suvm muzx ymgf onqc'

def send_confirmation_email(to_email, name):
    subject = "Health Camp Registration Confirmed"
    body = f"""
    Hi {name},

    Thank you for registering for the Free Health Camp at Care Point Hospital!

    📅 Date: April 20–21, 2025  
    🕘 Time: 9:00 AM – 5:00 PM  
    📍 Venue: Care Point Hospital Campus

    We look forward to seeing you there! Stay healthy and safe. 😊

    Regards,  
    Care Point Hospital
    """

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'pinkisuthar929@gmail.com'
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def home():
    return render_template('healthcampus.html', message=None)

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    city = request.form.get('city')

    # Save to CSV
    file_exists = os.path.isfile('registrations.csv')
    with open('registrations.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Phone', 'City'])
        writer.writerow([name, email, phone, city])

    # Send email
    send_confirmation_email(email, name)

    message = f"Thank you for registering, {name}!"
    return render_template('healthcampus.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
