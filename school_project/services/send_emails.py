import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_recover(subject, body, to_email):
    from_email = "#"
    password = "#"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
    except Exception as e:
        print(f"{e}")
