import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email(recipient, subject, body):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = recipient

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, [recipient], msg.as_string())
    return f"Email sent to {recipient}"

def register_send_email_tool(mcp):
    @mcp.tool("send_email")
    def send_email_tool(recipient: str, subject: str, body: str):
        """
        Send an email to anyone.
        SMTP server details and credentials are read from environment variables.
        """
        return send_email(recipient, subject, body)