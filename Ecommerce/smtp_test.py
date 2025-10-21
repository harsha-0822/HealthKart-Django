import smtplib
from email.mime.text import MIMEText

def test_smtp_connection():
    try:
        smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server address
        smtp_port = 587  # Replace with your SMTP port
        sender_email = 'Smharshavardhan08@gmail.com '  # Replace with your email address
        password = 'Harsha@81181981'  # Replace with your email password

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

        recipient_email = 'recipient@example.com'  # Replace with recipient's email address
        subject = 'Test Email'
        body = 'This is a test email sent from Python.'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Call the function to test the connection
test_smtp_connection()

# Email settings
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.your-email-provider.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'smharshavardhan08@gmail.com'
#EMAIL_HOST_PASSWORD = 'rdcp svzm ezxr wgzf'
