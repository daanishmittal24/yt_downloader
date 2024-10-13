import yagmail

sender_email = "mrolaf2403@gmail.com"
sender_password = "Mitt@lll"  # Use an app password if 2FA is enabled

yag = yagmail.SMTP(sender_email, sender_password)

try:
    yag.send(to="daanishmittal24@example.com", subject="Test Email", contents="This is a test email.")
    print("Email sent successfully.")
except Exception as e:
    print(f"Error: {e}")
