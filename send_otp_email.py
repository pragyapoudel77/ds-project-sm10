import smtplib

def send_email(sender, receiver, subject, message_body, smtp_server, smtp_port, smtp_username, smtp_password):
    message = f"""\
    Subject: {subject}
    To: {receiver}
    From: {sender}

    {message_body}"""

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender, receiver, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

# Example usage:
sender_email = input("Enter sender email address (e.g., Private Person <from@example.com>): ")
receiver_email = input("Enter receiver email address (e.g., A Test User <to@example.com>): ")
subject = input("Enter email subject: ")
message = input("Enter email message: ")

smtp_server = "sandbox.smtp.mailtrap.io"
smtp_port = 465
smtp_username = "8cf4fd595511ee"
smtp_password = "8b9355ae0d2b48"

send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, smtp_username, smtp_password)
