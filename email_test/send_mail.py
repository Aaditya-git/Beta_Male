import os
import ssl
from email.message import EmailMessage
import smtplib



def send_mail_to_test_beta():
    email_sender = 'aadityab134@gmail.com'
    email_password = os.environ.get('EMAIL_PASS')
    email_receiver = 'bamey2241997@gmail.com'
    print(f'Email Password: {email_password}')

    subject = 'TESTING BETA MALE VOICE COMMANDS'

    body = """Check out this generated email from BETA MALE project"""

    em = EmailMessage()

    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())
